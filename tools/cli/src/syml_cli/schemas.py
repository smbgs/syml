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
        # TODO: separately show stuff :)
        #self.console.print(result)
        self.console.print()

        for info in result.get('info'):
            self.console.print(
                '   • ' + Template(info.get('message')).substitute(info)
            )

        self.console.print()

        for error in result.get('errors'):
            self.console.print(
                '  🐛 ' + Template(error.get('message')).substitute(error),
                style='red'
            )

        validation = result['data'].get('validation')
        self.console.print()

        schema = StringIO()
        yaml.dump(validation.get('instance'), schema, sort_keys=False)
        schema.seek(0)

        self.console.print(
            '  🚩' + validation.get('message'),
            style='bold red'
        )
        self.console.print()
        syntax = Syntax(schema.read(), "yaml", theme="monokai", line_numbers=True)

        self.console.print(syntax)


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

        self.console.print_errors(result.get('errors'))
