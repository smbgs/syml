import asyncio
import json
import logging
import typing
from asyncio import StreamWriter, StreamReader, Task, Future, AbstractEventLoop
from subprocess import Popen
from threading import Thread
from typing import Dict

from syml_core import TOOLS_ROOT
from syml_core.service_base.base import LocalServiceBase
from syml_core.service_base.protocol import SymlServiceResponse, \
    SymlServiceCommand


class ServiceClient(LocalServiceBase):
    logger = logging.getLogger('ServiceClient')

    shared_loop = asyncio.new_event_loop()
    shared_loop_ref_cnt = 0

    def __init__(self, name, executable=None, loop=None):
        super().__init__(name)

        if executable is None:
            executable = TOOLS_ROOT / name / 'src' / 'server.py'

        self.local_executable = executable

        if loop is None:
            ServiceClient.shared_loop_ref_cnt += 1

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
            response = json.loads(raw_command)
            self.logger.debug("received serv response %s", response)
            cid = response.get('cid')
            if cid in self.active_commands:
                self.active_commands[cid].set_result(response)
                self.logger.debug("setting result %s %s", cid, response)
                del self.active_commands[cid]

    def disconnect(self):
        # TODO: shutdown command for local case (server)
        # self.wrapped_await(self.command({'type': 'disconnect'}))

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

    async def command(
        self,
        name,
        args: dict = None,
        shape=None,
        info=True,
        errors=True,
        pending=None
    ):

        pending = pending or Future()

        if not self.connecting:
            await self.connect()

        if not self.active:
            self.pending_commands.append((name, args, pending))
            return pending

        if args is None:
            args = {}

        command = SymlServiceCommand(
            name=name,
            # TODO: handle this case
            args=args,
            shape=shape,
            info=info,
            errors=errors,
        )

        self.active_commands[command.cid] = pending

        logging.debug("sending command %s %s", name, command)

        self.writer.write(command.jsonb())
        self.writer.write('\n'.encode())
        await self.writer.drain()

        return pending

    def wrapped_await(self, task) -> SymlServiceResponse:
        return asyncio.run_coroutine_threadsafe(task, self.loop).result()

    def __getattr__(self, name):
        async def async_wrapper(**kwargs):
            return await (await self.command(name=name, **kwargs))

        def wrapper(**kwargs):
            return self.wrapped_await(async_wrapper(**kwargs))

        return wrapper

    def sync_command(
        self,
        name: str,
        args: dict = None,
        shape: typing.List = None,
        info=True,
        errors=True,
    ):
        async def async_wrapper(**kwargs):
            return await (await self.command(**kwargs))

        return self.wrapped_await(async_wrapper(
            name=name,
            args=args,
            shape=shape,
            info=info,
            errors=errors,
        ))

    def finalize(self):
        self.logger.debug("finalizing %s", self._name)
        self.disconnect()

        ServiceClient.shared_loop_ref_cnt -= 1
        if ServiceClient.shared_loop_ref_cnt == 0:
            self.logger.debug("stopping event loop")

            async def stop():
                ServiceClient.shared_loop.stop()

            asyncio.run_coroutine_threadsafe(stop(), self.loop)

        self.logger.debug("finalized %s", self._name)

    def start_local_server(self):
        # TODO: if non-local shortcut should be conditional
        # TODO: docker and remote versions of this might be easy to do as well
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
