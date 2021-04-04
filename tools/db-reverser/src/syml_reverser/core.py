from os import getenv

import yaml
from sqlalchemy import MetaData, create_engine

CONNECTION_URI = getenv("DB_REVERSER_CONNECTION_URI", "postgresql://postgres:password@localhost:5432/")


class DBReverser:
    def __init__(self, connection_uri=None, engine=None):
        self.connection_uri = connection_uri
        self.engine = engine or create_engine(self.connection_uri)
        self.metadata = MetaData()

        self.metadata.reflect(engine)

    def get_tables(self):
        return self.metadata.tables.values()

    def get_transformed_tables(self):
        tables = {}

        for table in self.get_tables():
            tables[str(table.name)] = []

            for column in table.columns.values():
                column_info = {
                    'name': str(column.name),
                    'type': str(column.type)
                }

                if bool(column.primary_key):
                    column_info['primary'] = True

                tables[str(table.name)].append(column_info)

        return tables

    def generate_yaml(self, path='tables.yaml'):
        yaml_dict = {
            'tables': self.get_transformed_tables()
        }

        with open(path, 'w') as file:
            yaml.dump(yaml_dict, file)


if __name__ == '__main__':
    engine = create_engine(CONNECTION_URI)

    obj = DBReverser(engine=engine)
    obj.generate_yaml()
