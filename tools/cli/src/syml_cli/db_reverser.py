import asyncio

from syml_cli.clients.db_reverser import SymlDBReverserClient
from syml_cli.common import SymlServiceBasedCLI


class SymlDBReverserCLI(SymlServiceBasedCLI):

    def __init__(self):
        self._db_reverser = SymlDBReverserClient()
        super().__init__()

    def alchemy(
        self,

        # DB Reverser parameters
        connection_string,
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

        # TODO: pass to serialization service
        yield result
