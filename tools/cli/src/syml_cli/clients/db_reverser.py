from syml_cli.common import SYML_ROOT_PATH
from syml_core.service_base.local import CLIClient


class SymlDBReverserClient(CLIClient):

    local_executable = \
        SYML_ROOT_PATH / 'db-reverser' / 'src' / 'db_reverser_service.py'

    def __init__(self):
        # TODO: this should not be a service, probably?
        super().__init__('db-reverser')
