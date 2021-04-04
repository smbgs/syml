from os import getenv

from sqlalchemy import MetaData, create_engine

CONNECTION_URI = getenv("DB_REVERSER_CONNECTION_URI", "postgresql://postgres:password@localhost:5432/")


class DBReverser:
    def __init__(self, connection_uri=None, engine=None, schema="public", views=False):
        self.connection_uri = connection_uri
        self.engine = engine or create_engine(self.connection_uri)
        self.metadata = MetaData(self.engine, schema=schema)

        self.metadata.reflect(views=views)

    def get_tables(self):
        return self.metadata.tables.values()

    def get_transformed_tables(self):
        tables = {}

        for table in self.get_tables():
            tables[str(table.name)] = []

            for column in table.columns.values():
                column_info = {
                    'name': str(column.name),
                    'type': str(column.type),
                    'primary': bool(column.primary_key)
                }

                tables[str(table.name)].append(column_info)

        return tables


if __name__ == '__main__':
    engine = create_engine(CONNECTION_URI)

    obj = DBReverser(engine=engine)
