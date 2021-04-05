import asyncio
import json
import logging
from asyncio import StreamWriter, StreamReader, Task, Future, AbstractEventLoop
from pathlib import Path
from string import Template
from subprocess import Popen
from threading import Thread
from typing import Dict
from uuid import uuid4

import yaml
import subprocess

class LocalServiceBase:
    # TODO: we need to add support for data "shapes" similar to graphql
    # so that we can calculate and return only things that client asked for

    logger = logging.getLogger('LocalServiceBase')

    # TODO: consider making this configurable
    SYML_ENVIRONMENTS_PATH = '~/.syml/environments.yaml'
    UNIX_SOCKET_PATH = '~/.syml/sockets/${service}.sock'

    local_executable: Path

    def __init__(self, name):
        self._name = name
        self.local_server = None

    async def on_client_connected(
        self,
        reader: StreamReader,
        writer: StreamWriter
    ):
        self.logger.debug('client connected')
        while True:  # TODO: while active instead
            raw_command = await reader.readline()

            if raw_command == b'':
                await asyncio.sleep(0.5)
                continue

            try:
                command = json.loads(raw_command)
                logging.debug("received command %s", command)

                name = command.pop('name')
                cid = command.pop('cid', None)

                callable_command = getattr(self, f'cmd_{name}')

                # TODO: more safety, error handling etc... schemas?
                # TODO: handle generators
                result = await callable_command(**command)
                response = {
                    'cid': uuid4().hex,
                    'result': result
                }

                if cid:
                    response['rid'] = cid

                # TODO: dispatch command and handle it
                # TODO: handle internal \n in the payload, base64?
                writer.write(json.dumps(
                    response,
                    default=lambda o: o.json() if hasattr(o, 'json') else str(o)
                ).encode())
                writer.write('\n'.encode())

                logging.debug("sending response %s", response)

                await writer.drain()
            except Exception as e:
                self.logger.exception("oh no", e)

    async def cmd_disconnect(self):
        pass

    @classmethod
    def resolve_service_path(cls, name: str):
        return Path(
            Template(cls.UNIX_SOCKET_PATH).substitute({"service": name})
        ).expanduser().resolve()

    async def serve(self, path):
        server = await asyncio.start_unix_server(
            self.on_client_connected,
            path=path
        )

        async with server:
            await server.serve_forever()

    def unix_serve(self):
        self.logger.debug('starting server %s', self._name)
        path = self.resolve_service_path(self._name)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        asyncio.run(self.serve(path))

    def get_pipenv_python_bin(self, executable_path):
        return subprocess.run([
            'pipenv',
            '--py',
            executable_path
        ])

    def start_local_server(self):
        # TODO: if non-local shortcut should be conditional
        # TODO: docker and remote versions of this might be easy to do as well

        # env_config_path = Path(self.SYML_ENVIRONMENTS_PATH).expanduser().resolve()
        # if env_config_path.exists():
        #     with open(str(env_config_path), 'r+') as f:
        #         env_config = yaml.load(f, Loader=yaml.SafeLoader)
        #         python_bin = env_config.get(self._name)
        #         if not python_bin:
        #
        # else:


        self.logger.debug('Starting local service %s', self._name)
        self.local_server = Popen(
            cwd=str(self.local_executable.parent),
            args=[
                'pipenv',
                'run',
                'python',
                str(self.local_executable),
            ],
        )
        self.logger.debug('Started local service %s', self._name)


class CLIClient(LocalServiceBase):
    logger = logging.getLogger('CLICLient')

    shared_loop = asyncio.new_event_loop()
    shared_loop_ref_cnt = 0

    def __init__(self, name, loop=None):
        super().__init__(name)

        if loop is None:
            CLIClient.shared_loop_ref_cnt += 1

        self.loop: AbstractEventLoop = loop or self.shared_loop
        self.reader: StreamReader = None
        self.writer: StreamWriter = None
        self.connecting = False
        self.active = False
        self.reader_task: Task = None
        self.pending_commands = []
        self.active_commands: Dict[str, Future] = {}

        def commands():
            asyncio.set_event_loop(self.loop)
            if not self.shared_loop.is_running():
                logging.debug("Starting thread loop")
                self.shared_loop.run_forever()
            logging.debug("Thread loop stopped")

        t = Thread(target=commands)
        t.start()

    async def connect(self):
        self.logger.debug('Connecting to %s...', self._name)

        had_failure = False
        while True:
            try:
                self.reader, self.writer = await asyncio.open_unix_connection(
                    path=self.resolve_service_path(self._name)
                )
                break
            except (ConnectionRefusedError, FileNotFoundError):
                if had_failure:
                    self.logger.debug('Unable to connect... retrying')
                else:
                    self.start_local_server()
                await asyncio.sleep(0.25)
                had_failure = True

        self.active = True
        self.reader_task = asyncio.create_task(self.read_responses())

        if self.pending_commands:
            for name, arguments, pending in self.pending_commands:
                await self.command(name, arguments, pending)

    async def read_responses(self):
        while self.active:
            raw_command = await self.reader.readline()
            command = json.loads(raw_command)
            self.logger.debug("received serv command %s", command)
            rid = command.get('rid')
            if rid in self.active_commands:
                self.active_commands[rid].set_result(command['result'])
                self.logger.debug("setting result %s %s", rid, command)
                del self.active_commands[rid]

    def disconnect(self):
        # TODO: shutdown command for local case (server)
        #self.wrapped_await(self.command({'type': 'disconnect'}))

        self.active = False
        if self.reader_task:
            self.writer.close()
            self.reader_task.cancel()
            self.logger.debug("closed the writer and reader")

        if self.local_server:
            self.logger.debug("Terminating the local command server process %s",
                              self._name)
            # TODO: it might be useful to not shutdown the process
            # only do this if graceful shutdown failed tho, for now
            # kill immediately
            self.local_server.terminate()

    async def command(self, name, arguments: dict = None, pending=None):

        pending = pending or Future()

        if not self.connecting:
            await self.connect()

        if not self.active:
            self.pending_commands.append((name, arguments, pending))
            return pending

        if arguments is None:
            arguments = {}

        arguments['cid'] = uuid4().hex
        self.active_commands[arguments['cid']] = pending

        logging.debug("sending command %s %s", name, arguments)
        command = {**arguments, "name": name}
        self.writer.write(json.dumps(
            command,
            default=lambda o: o.json() if hasattr(o, 'json') else str(o)
        ).encode())
        self.writer.write('\n'.encode())
        await self.writer.drain()

        return pending

    def wrapped_await(self, task):
        return asyncio.run_coroutine_threadsafe(task, self.loop).result()

    def __getattr__(self, item):
        async def async_wrapper(arguments):
            return await (await self.command(item, arguments))

        def wrapper(**kwargs):
            return self.wrapped_await(async_wrapper(kwargs))

        return wrapper

    def finalize(self):
        self.logger.debug("finalizing %s", self._name)
        self.disconnect()

        CLIClient.shared_loop_ref_cnt -= 1
        if CLIClient.shared_loop_ref_cnt == 0:
            self.logger.debug("stopping event loop")

            async def stop():
                CLIClient.shared_loop.stop()

            asyncio.run_coroutine_threadsafe(stop(), self.loop)

        self.logger.debug("finalized %s", self._name)


