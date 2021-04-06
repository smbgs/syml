from os import getenv

from syml_core.service_base.local import LocalServiceBase
from sqlalchemy import MetaData, create_engine, ForeignKeyConstraint, ForeignKey

from syml_core.service_base.protocol import SymlServiceResponse


class SymlDBReverserService(LocalServiceBase):

    def __init__(self):
        # TODO: this should not be a service, probably?
        super().__init__('db-reverser')

    async def cmd_alchemy(
        self,
        connection_string,
        schemas,
        objects_names,
        objects_types,
    ):

        if connection_string == '@postgres':
            connection_string = "postgresql://postgres:password@localhost:5432/symltest"
            # TODO: postgres in the docker locally or something like that?
            # https://pypi.org/project/pyembedpg/ kinda sucks :(

        engine = create_engine(connection_string)

        if schemas == '@all':
            # TODO: adjust this if necessary with the schema filter
            pass

        metadata = MetaData(engine)

        # TODO: check if we can get schema list instead
        #self.metadata = MetaData(engine, schema=schema)

        # TODO: support for views, and other object types
        if objects_names != '@all':
            metadata.reflect(only=objects_names.split(','))
        else:
            metadata.reflect()

        # TODO:  filter tables by schema name maybe? probably not gonna work :(
        return SymlServiceResponse(
            data=self.get_transformed_tables(metadata),
        )

    @staticmethod
    def get_transformed_tables(metadata):
        tables = {}

        for table_name, table in metadata.tables.items():
            tables[table_name] = []

            foreign_keys = {}

            fk: ForeignKey
            for fk in table.foreign_keys:
                foreign_keys[fk.column.name] = fk

            # TODO: this shape needs to be a bit tweaked to support views
            # and constraints, indexes and fkeys
            for column in table.columns.values():
                column_info = {
                    'name': str(column.name),
                    'type': str(column.type),

                }

                tags = set()

                if column.primary_key:
                    tags.add('primary_key')

                if column.nullable:
                    tags.add('nullable')

                if tags:
                    column_info['tags'] = list(tags)

                if column.name in foreign_keys:
                    column_info['reference'] = {
                        'table': foreign_keys[column.name].column.table.name,
                        'column': foreign_keys[column.name].column.name
                    }

                tables[str(table.name)].append(column_info)

        return tables
