from rich.console import Console

from syml_cli.clients import Clients
from syml_cli.common import SymlServiceBasedCLI

console = Console()


class SymlSchemasCLI(SymlServiceBasedCLI):
    """
    Schemas commands validate schemas
    """

    def __init__(self):
        self._schemas = Clients.schemas

        super().__init__()

    def validate(
        self,
        schema_path: str,
    ):
        """
        Connects to the database and reverses the specified objects using the
        specified `output` format to the specified `stream`

        :param schema_path:
            Path or URL to SYML Schema Definition
        """
        result = self._schemas.sync_command(
            name='validate',
            args=dict(
                path=schema_path,
            ),
            shape=[
                'message',
                'absolute_path',
                'instance',
                'validator',
                'validator_value',
            ]
        )

        console.print(result)
