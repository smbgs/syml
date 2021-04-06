from syml_cli.common import SYML_ROOT_PATH
from syml_core.service_base.client import CLIClient


class SymlSchemasClient(CLIClient):

    local_executable = \
        SYML_ROOT_PATH / 'schemas' / 'src' / 'schemas_service.py'

    def __init__(self):
        super().__init__('schemas')
