from os import getenv

from sqlalchemy import create_engine

CONNECTION_URI = getenv('DB_PULSE_SNOWFLAKE_CONNECTION_URI',
                        "postgresql+asyncpg://scott:tiger@localhost/test")


def retreive_snowflake_data(config):
    engine = create_engine(CONNECTION_URI, echo=False)

    with engine.connect() as conn:
        conn.execute(

        )
