import asyncio

from syml_cli.common import SYML_CLI_PATH
from syml_core.service_base.local import CLIClient


class SymlProfileClient(CLIClient):

    def __init__(self):
        # TODO: this should not be a service, probably?
        super().__init__('profiles')

        asyncio.run_coroutine_threadsafe(
            self.connect(
                local_executable=
                SYML_CLI_PATH / 'src' / 'profiles_service.py'
            ),
            loop=self.loop
        )

