from sqlalchemy import MetaData, create_engine, ForeignKey, ForeignKeyConstraint, CheckConstraint, UniqueConstraint

from syml_core.service_base.base import LocalServiceBase
from syml_core.service_base.protocol import SymlServiceResponse, \
    SymlServiceCommand
from syml_db_reverser.service.parameters import ReverseUsingAlchemy
from syml_db_reverser.service.types import TableEntity, SpecTable, ColumnEntity, Constraints, ForeignKeyConstraintType, \
    CheckConstraintType


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
        # self.metadata = MetaData(engine, schema=schema)

        # TODO: support for views, and other object types
        if objects_names != '@all':
            metadata.reflect(only=objects_names.split(','))
        else:
            metadata.reflect()

        return metadata

    def create_constraint_list_if_not_exist(self, constraints: Constraints, key: str):
        if getattr(constraints, key) is None:
            setattr(constraints, key, [])


    async def cmd_lol(self, cmd: SymlServiceCommand[ReverseUsingAlchemy]):
        metadata = self.get_database_metadata(
            connection_string=cmd.args.connection_string,
            schemas=cmd.args.schemas,
            objects_names=cmd.args.objects_names,
            objects_types=cmd.args.objects_types,
        )

        entities: list[TableEntity] = []

        for table in metadata.tables.values():
            columns: list[ColumnEntity] = []
            constraints = Constraints()

            for constraint in table.constraints:
                if isinstance(constraint, ForeignKeyConstraint):
                    self.create_constraint_list_if_not_exist(constraints, 'foreignKeys')

                    constraints.foreignKeys.append(ForeignKeyConstraintType(
                        name=constraint.name,
                        columnNames=constraint.column_keys,
                        elements=[element.target_fullname for element in constraint.elements],
                        onDelete=constraint.ondelete,
                        onUpdate=constraint.onupdate,
                        matchFull=constraint.match
                    ))

                if isinstance(constraint, CheckConstraint):
                    self.create_constraint_list_if_not_exist(constraints, 'check')

                    constraints.check.append(CheckConstraintType(
                        name=constraint.name,
                        condition=constraint.sqltext.text
                    ))

                if isinstance(constraint, UniqueConstraint):
                    self.create_constraint_list_if_not_exist(constraints, 'unique')
                    for constraint_unique_column in constraint.columns.values():
                        getattr(constraints, 'unique').append(constraint_unique_column.name)

            for column in table.columns.values():
                constraint_column_types = {
                    'primary_key': 'primaryKey',
                    'nullable': 'nullable',
                    'autoincrement': 'autoincrement',
                }

                for original_constraint_key, constraint_name in constraint_column_types.items():
                    if getattr(column, original_constraint_key):
                        self.create_constraint_list_if_not_exist(constraints, constraint_name)
                        getattr(constraints, constraint_name).append(column.name)

                column_entity = ColumnEntity(
                    name=column.name,
                    type=str(column.type),
                )

                columns.append(column_entity)

            entity_spec = SpecTable(
                columns=columns,
                constraints=constraints
            )

            entity = TableEntity(
                name=table.name,
                description=table.description,
                spec=entity_spec
            )

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
