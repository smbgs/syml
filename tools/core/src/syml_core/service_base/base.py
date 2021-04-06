import asyncio
import json
import logging
import subprocess
from asyncio.streams import StreamReader, StreamWriter
from pathlib import Path
from string import Template
from subprocess import Popen
from uuid import uuid4

from syml_core.service_base.protocol import SymlServiceCommand, \
    SymlServiceResponse


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
                command = SymlServiceCommand.parse(raw_command)
                logging.debug("received command %s", command)

                callable_command = getattr(self, f'cmd_{command.name}')

                # TODO: handle generators
                response: SymlServiceResponse = await callable_command(command)
                response.command = command

                writer.write(response.jsonb())
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
