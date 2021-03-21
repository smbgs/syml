from os import getenv

from sqlalchemy import MetaData, create_engine

CONNECTION_URI = getenv("DB_REVERSER_CONNECTION_URI", "postgresql://postgres:password@localhost:5432/")


def main():
    engine = create_engine(CONNECTION_URI)
    metadata = MetaData()
    metadata.reflect(engine)

    if len(metadata.tables) == 0:
        print("Tables not found *o*")
    else:
        print(f'{len(metadata.tables)} tables was detected!\n')

    for table in metadata.tables.values():
        print(table.name)
        for column in table.columns.values():
            print(f'  {"*" if column.primary_key else ""}{column.name} - {None if column.type._isnull else column.type}')
        print("------------------------")


if __name__ == '__main__':
    main()
