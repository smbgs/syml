from sqlalchemy import MetaData, create_engine, ForeignKey

from syml_core.service_base.base import LocalServiceBase
from syml_core.service_base.protocol import SymlServiceResponse, \
    SymlServiceCommand
from syml_db_reverser.service.parameters import ReverseUsingAlchemy


class SymlDBReverserService(LocalServiceBase):

    def __init__(self):
        # TODO: this should not be a service, probably?
        super().__init__('db-reverser')

    def get_database_metadata(self, connection_string, schemas, objects_names, objects_types):
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

        return metadata

    async def cmd_lol(self, cmd: SymlServiceCommand[ReverseUsingAlchemy]):
        metadata = self.get_database_metadata(
            connection_string=cmd.args.connection_string,
            schemas=cmd.args.schemas,
            objects_names=cmd.args.objects_names,
            objects_types=cmd.args.objects_types,
        )

        entities = []

        for table in metadata.tables.values():
            columns = []

            for column in table.columns.values():
                constraints = []
                constraintTypes = {
                    'primary_key': 'pk',
                    'nullable': 'nullable', #TODO: Add unique
                    'autoincrement': 'autoincrement',
                    'inherit_cache': 'inherit-cache',
                    'is_clause_element': 'clause-element',
                    'is_literal': 'literal',
                    'is_selectable': 'selectable',
                    'supports_execution': 'supports-execution',
                    'system': 'system',
                    'uses_inspection': 'uses-inspection',
                }

                for originalConstraint, constraint in constraintTypes.items():
                    if getattr(column, originalConstraint) is True:
                        constraints.append(constraint)

                entity_column = {
                    'name': column.name,
                    'type': str(column.type),
                    'constraints': constraints,
                }

                columns.append(entity_column)

            entity = {
                'kind': 'database',
                'provider': 'postgres', # TODO: INSERT DB TYPE
                'type': 'table',
                'name': table.name,
                'description': table.description,
                'spec': {
                    'database': 'database_name', # TODO: INSERT DB
                    'columns': columns,
                    'constraints': []
                },
            }

            entities.append(entity)

        return SymlServiceResponse(
            data=entities,
        )

    async def cmd_alchemy(self, cmd: SymlServiceCommand[ReverseUsingAlchemy]):
        metadata = self.get_database_metadata(
            connection_string=cmd.args.connection_string,
            schemas=cmd.args.schemas,
            objects_names=cmd.args.objects_names,
            objects_types=cmd.args.objects_types,
        )

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
