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


class LocalServiceBase:
    # TODO: consider making this configurable
    UNIX_SOCKET_PATH = '~/.syml/sockets/${service}.sock'

    logger = logging.getLogger('LocalServiceBase')

    def __init__(self, name):
        self._name = name

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
                writer.write(json.dumps(response).encode())
                writer.write('\n'.encode())

                await writer.drain()
            except Exception as e:
                self.logger.exception("oh no")

    async def cmd_disconnect(self):
        pass

    def resolve_service_path(self, name: str):
        return Template(self.UNIX_SOCKET_PATH).substitute({"service": name})

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
        self.active = False
        self.reader_task: Task = None
        self.local_server = None
        self.pending_commands = []
        self.active_commands: Dict[str, Future] = {}

        def commands():
            asyncio.set_event_loop(self.loop)
            if not self.loop.is_running():
                self.loop.run_forever()

        t = Thread(target=commands)
        t.start()

    async def connect(self, local_executable=None):

        # TODO: if non-local shortcut should be conditional
        # TODO: docker and remote versions of this might be easy to do as well
        self.logger.debug('Starting local service %s', self._name)
        if local_executable:
            self.local_server = Popen([
                'pipenv',
                'run',
                'python',
                str(local_executable),
            ])

        self.logger.debug('Connecting to %s...', self._name)

        had_failure = False
        while True:
            try:
                self.reader, self.writer = await asyncio.open_unix_connection(
                    path=self.resolve_service_path(self._name)
                )
                break
            except ConnectionRefusedError:
                if had_failure:
                    self.logger.debug('Unable to connect... retrying')
                await asyncio.sleep(1)
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
        self.wrapped_await(self.command({'type': 'disconnect'}))

        self.active = False
        if self.reader_task:
            self.reader_task.cancel()

        if self.local_server:
            self.logger.debug("Terminating the local command server process %s",
                              self._name)
            # TODO: it might be useful to not shutdown the process
            # only do this if graceful shutdown failed tho, for now
            # kill immediately
            self.local_server.terminate()

    async def command(self, name, arguments: dict = None, pending=None):

        pending = pending or Future()

        if not self.active:
            self.pending_commands.append((name, arguments, pending))
            return pending

        if arguments is None:
            arguments = {}

        arguments['cid'] = uuid4().hex
        self.active_commands[arguments['cid']] = pending

        logging.debug("sending command %s %s", name, arguments)
        command = {**arguments, "name": name}
        self.writer.write(json.dumps(command).encode())
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
        self.disconnect()
        CLIClient.shared_loop_ref_cnt -= 1
        if CLIClient.shared_loop_ref_cnt == 0:
            CLIClient.shared_loop.stop()
