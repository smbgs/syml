from io import StringIO
from string import Template

import yaml
from rich.syntax import Syntax

from syml_cli.clients import Clients
from syml_cli.common import SymlServiceBasedCLI


class SymlSchemasCLI(SymlServiceBasedCLI):
    """
    Schemas commands validate schemas
    """

    def get(self, schema_path: str, validate=False):
        result = Clients.schemas.sync_command(
            name='get',
            args=dict(
                path=schema_path,
                validate=validate,
            )
        )

        self.console.print()

        self.console.print_info(result.get('info'))

        schema = StringIO()
        yaml.dump(result['data'].get('definition'), schema, sort_keys=False)
        schema.seek(0)
        syntax = Syntax(schema.read(), "yaml", theme="native", line_numbers=True)
        self.console.print()
        self.console.print(syntax)

        self.console.print_errors(result.get('errors'))
        if validate:
            validation = result['data'].get('validation')
            self._print_validation(validation)

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
        result = Clients.schemas.sync_command(
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

        self.console.print()

        self.console.print_info(result.get('info'))
        self.console.print_errors(result.get('errors'))
        self._print_validation(result.get('data'))

    def _print_validation(self, validation):

        schema = StringIO()
        yaml.dump(validation.get('instance'), schema, sort_keys=False)
        schema.seek(0)

        # for error in result.get('errors'):
        #     self.console.print(
        #         '  🐛 ' + Template(error.get('message')).substitute(error),
        #         style='red'
        #     )

        self.console.print(
            '  🚩' + validation.get('message'),
            style='bold red'
        )
        self.console.print()

        syntax = Syntax(schema.read(), "yaml", theme="native", line_numbers=True)
        self.console.print(syntax)
