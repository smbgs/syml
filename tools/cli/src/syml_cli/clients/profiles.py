from syml_cli.common import SYML_CLI_PATH
from syml_core.service_base.client import CLIClient


class SymlProfileClient(CLIClient):

    local_executable = SYML_CLI_PATH / 'src' / 'profiles_service.py'

    def __init__(self):
        # TODO: this should not be a service, probably?
        super().__init__('profiles')
