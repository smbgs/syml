import asyncio
import logging
import subprocess
import traceback
from asyncio.streams import StreamReader, StreamWriter
from pathlib import Path
from string import Template
from typing import get_type_hints, get_args

from syml_core.service_base.protocol import SymlServiceCommand, \
    SymlServiceResponse


class LocalServiceBase:
    # TODO: we need to add support for data "shapes" similar to graphql
    # so that we can calculate and return only things that client asked for

    logger = logging.getLogger('LocalServiceBase')

    # TODO: consider making this configurable
    SYML_ENVIRONMENTS_PATH = '~/.syml/environments.yaml'
    UNIX_SOCKET_PATH = '~/.syml/sockets/${service}.sock'

    def __init__(self, name: str):
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
                # TODO: not ideal, remove pooling if possible
                await asyncio.sleep(0.5)
                continue

            try:

                command = SymlServiceCommand.parse(raw_command)

                logging.debug("received command %s", command)
                callable_command = getattr(self, f'cmd_{command.name}')

                cmd_arg = get_type_hints(callable_command).get('cmd')

                if cmd_arg:
                    args_type = get_args(cmd_arg)[0]
                    command.args = args_type(**command.args)

                # TODO: handle generators
                try:
                    response: SymlServiceResponse
                    if cmd_arg:
                        response = await callable_command(command)
                    else:
                        response = await callable_command()

                except Exception as e:
                    response = SymlServiceResponse(
                        data=dict(),
                        errors=[
                            dict(message="unhandled exception while "
                                         "processing command",
                                 exception=e,
                                 trace=traceback.format_exc().splitlines()
                            )
                        ]
                    )

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

    @staticmethod
    def get_pipenv_python_bin(executable_path):
        return subprocess.run([
            'pipenv',
            '--py',
            executable_path
        ])

