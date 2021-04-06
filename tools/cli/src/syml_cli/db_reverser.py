import colorama
import sys
import yaml
from rich import box
from rich.console import Console
from rich.table import Table

from syml_cli.clients.db_reverser import SymlDBReverserClient
from syml_cli.common import SymlServiceBasedCLI

console = Console()

class SymlDBReverserCLI(SymlServiceBasedCLI):

    def __init__(self):
        self._db_reverser = SymlDBReverserClient()
        super().__init__()

    def alchemy(
        self,

        # DB Reverser parameters
        connection_string='@postgres',
        schemas='@all',
        objects_names='@all',
        objects_types='@all',

        # DB Schema Serializer parameters
        output='yaml',
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
            Output format (yaml, markdown, etc.)

        :param stream:
            Output destination (@stdout|-, uri) to serialize the output into

        """
        result = self._db_reverser.alchemy(
            connection_string=connection_string,
            schemas=schemas,
            objects_names=objects_names,
            objects_types=objects_types,
        )
        colorama.init()

        # TODO: pass to serialization service
        for name, manifest in result['data'].items():

            table = Table(
                title=f'  {name}',
                title_justify='left',
                title_style='bold white reverse',
                show_header=True,
                header_style="bold white",
                box=box.SQUARE
            )

            table.add_column(" :key:", justify="center", width=3)
            table.add_column("Name", style="dim")
            table.add_column("Type", justify="left")
            table.add_column("N", justify="right")
            table.add_column("Reference", justify="right")

            for field in manifest:
                table.add_row(
                    "✔️" if 'primary_key' in field.get('tags', []) else "",

                    f"[bold]{field['name']}[/bold]"
                    if 'primary_key' in field.get('tags', [])
                    else field['name'],

                    field['type'],
                    "✔️" if 'nullable' in field.get('tags', []) else "",
                    field['reference']['table'] if 'reference' in field else "",
                    style="#cccccc"
                )
                # yaml.dump(field, sys.stdout, sort_keys=False)

            console.print(table)
            yield '\n'
