from rich import box
from rich.table import Table

from syml_cli.clients import Clients
from syml_cli.common import SymlServiceBasedCLI


class SymlDBReverserCLI(SymlServiceBasedCLI):

    def alchemy(
        self,

        # DB Reverser parameters
        connection_string='@postgres',
        schemas='@all',
        objects_names='@all',
        objects_types='@all',

        # DB Schema Serializer parameters
        output='cli',
        stream='@stdout'
    ):
        """
        Connects to the database and reverses the specified objects using the
        specified `output` format to the specified `stream`

        :param connection_string:
            Database connection string.
            Note: use sqlalchemy format, i.e:
            `dialect+driver://username:password@host:port/database`

        :param schemas:
            Comma separated list of database schemas to reverse objects from

        :param objects_names:
            Comma separated list of database objects (tables, schemas, etc.)
            to reverse

        :param objects_types:
            Comma separated list of database objects types (table, schema, etc.)
            to reverse

        :param output:
            Output format (cli, yaml, markdown, etc.)

        :param stream:
            Output destination (@stdout|-, uri) to serialize the output into

        """
        result = Clients.db_reverser.alchemy(
            args=dict(
                connection_string=connection_string,
                schemas=schemas,
                objects_names=objects_names,
                objects_types=objects_types,
            )
        )

        # TODO: support various output types?

        if output == 'cli':

            self.console.print()

            for name, manifest in result['data'].items():

                table = Table(
                    title=f'  {name}',
                    title_justify='left',
                    title_style='bold white reverse',
                    show_header=True,
                    header_style="bold white",
                    expand=True,
                    box=box.SQUARE
                )

                table.add_column(" :key:", justify="center", max_width=3)
                table.add_column("Name", style="dim", min_width=30)
                table.add_column("Type", justify="left", min_width=15)
                table.add_column("N", justify="center", max_width=1)
                table.add_column("Reference", justify="right", min_width=20)

                for field in manifest:
                    table.add_row(
                        "✔️" if 'primary_key' in field.get('tags', []) else "",

                        f"[bold]{field['name']}[/bold]"
                        if 'primary_key' in field.get('tags', [])
                        else field['name'],

                        field['type'],
                        "✔️" if 'nullable' in field.get('tags', []) else "",

                        f"{field['reference']['table']}."
                        f"{field['reference']['column']}"

                        if 'reference' in field else "",

                        style="#cccccc"
                    )
                    # yaml.dump(field, sys.stdout, sort_keys=False)

                self.console.print(table)
                self.console.print()
