import copy
from io import StringIO

import yaml
from rich import box
from rich.console import RenderGroup
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

from syml_cli.gen.clients import Clients
from syml_cli.common import SymlServiceBasedCLI, CUSTOM


class SymlSchemasCLI(SymlServiceBasedCLI):
    """
    Schemas commands validate schemas
    """

    def get(self, schema_path: str, validate=False, output='cli'):
        result = Clients.schemas.sync_command(
            name='get',
            args=dict(
                path=schema_path,
                validate=validate,
            )
        )

        self.console.print()

        self.console.print_info(result.get('info'))

        data = result.get('data')

        if data:

            if output == 'cli':

                definition = data.get('definition')
                meta = definition.get('meta')
                spec = definition.get('spec')
                spec_fields = spec.get('fields')
                if 'source' in spec:
                    parent_source = spec.get('source')
                else:
                    parent_source = {}

                spec_target = spec.get('target')

                self.console.print()

                renderables = [
                    "",
                    "[bold]Meta:[/]",
                    f" [bold]type[/]: {meta.get('type')}",
                    f" [bold]version[/]: {meta.get('type')}",
                    f" [bold]description[/]: {meta.get('desc').strip()}",
                    "",
                ]

                if parent_source:
                    renderables += [
                        "[bold]Source:[/]",
                        f" [bold]alias[/]: {parent_source.get('alias')}",
                        f" [bold]schema[/]: {parent_source.get('schema')}",
                        "",
                    ]

                if spec_target:
                    spec_target_spec = spec_target.get('spec')
                    renderables += [
                        "[bold]Target:[/b]",
                        f" [bold]kind[/]: {spec_target.get('kind')}",
                        f" [bold]provider[/]: {spec_target.get('provider')}",
                        f" [bold]type[/]: {spec_target.get('type')}",
                        f" [bold]database[/]: {spec_target_spec.get('database')}",
                        f" [bold]schema[/]: {spec_target_spec.get('schema')}",
                        f" [bold]table[/]: {spec_target_spec.get('table')}",
                    ]

                # Print meta
                self.console.print(Panel(
                    RenderGroup(*renderables, ""),
                    title=meta.get('name'),
                    title_align='left',
                    box=box.ROUNDED,
                    padding=(0, 0, 0, 2)
                ))

                table = Table(
                    show_header=True,
                    header_style="bold white",
                    expand=True,
                    box=CUSTOM,
                    show_lines=True,
                )

                table.add_column(" :key:", justify="center", max_width=3)
                table.add_column("Name", style="dim", min_width=30)
                table.add_column("Dim", style="dim", min_width=10)
                table.add_column("Type", justify="left", min_width=15)
                table.add_column("N", justify="center", max_width=1)
                table.add_column("E", justify="center", max_width=1)
                table.add_column("Source", justify="left", min_width=15)
                table.add_column("Relation", justify="right", min_width=20)

                self._render_fields(parent_source, spec_fields, table)

                self.console.print(table)

                self.console.print()

            elif output == 'cli-yaml':
                schema = StringIO()
                yaml.dump(
                    result['data'].get('definition'), schema,
                    sort_keys=False
                )
                schema.seek(0)
                syntax = Syntax(
                    schema.read(), "yaml", theme="native",
                    line_numbers=True
                )
                self.console.print()
                self.console.print(syntax)

        self.console.print_errors(result.get('errors'))
        if validate:
            validation = result['data'].get('validation')
            self._print_validation(validation)

    def _render_fields(self, parent_source, spec_fields, table, level=0):
        for field in spec_fields:

            constraints = set(field.get('constraints', []))
            source = copy.copy(parent_source)
            fields = field.get('fields')

            if 'sourceField' in field:
                source['field'] = field['sourceField']
            else:
                source = field.get('source', source)

            table.add_row(
                "✔️" if 'pk' in constraints else "",

                "  " * level
                + ("‣ " if level > 0 else "")
                + (f"[bold]{field['name']}[/bold]"
                   if 'pk' in constraints else field['name']),

                field.get('dimension'),
                field['type'],

                "✔️" if 'not-null' not in constraints else "",

                "✔️" if 'not-empty' not in constraints else "",

                f"{source.get('alias')}.{source.get('field')}"
                if source else "",

                str(field.get('relation', "")),

                style="#cccccc" if field['type'] != 'GROUP' else "#ffffff bold"
            )

            if fields:
                self._render_fields(source, fields, table, level + 1)

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

        if validation.get('message'):
            schema = StringIO()
            yaml.dump(validation.get('instance'), schema, sort_keys=False)
            schema.seek(0)
            self.console.print(
                '  🚩' + validation.get('message'),
                style='bold red'
            )
            self.console.print()

            syntax = Syntax(schema.read(), "yaml", theme="native",
                            line_numbers=True)
            self.console.print(syntax)
        else:
            self.console.print(Panel("Schema is valid!", style="green"))
