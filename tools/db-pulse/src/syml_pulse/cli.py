import asyncio
import logging
from os import getenv
from pathlib import Path

import humanize
import yaml
from sqlalchemy.ext.asyncio import create_async_engine

from src.syml_pulse.core import watch_source_dest

CONNECTION_URI = getenv('DB_PULSE_CONNECTION_URI',
                        "postgresql+asyncpg://scott:tiger@localhost/test")


async def async_main(config):
    engine = create_async_engine(
        CONNECTION_URI, echo=False,
    )

    async with engine.connect() as conn:
        async for diff in watch_source_dest(
            conn,
            config.get('spec').get('mappings')
        ):
            print('- source {:70} ({:10} ~{:10} rows)'.format(
                diff.source_table,
                humanize.naturalsize(
                    abs(diff.source_stats.table_bytes), False, True, "%.3f"
                ),
                int(diff.source_stats.row_estimate),
            ))

            print('    dest {:70} ({:10} ~{:10} rows)'.format(
                diff.destination_table,
                humanize.naturalsize(
                    abs(diff.destination_stats.table_bytes), False, True, "%.3f"
                ),
                int(diff.destination_stats.row_estimate),
            ))

            print('')
        print('---------------------------------------------------------------')


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.INFO)

    with open(
        str(Path('../examples/elt-progress/simple.etl.syml.yaml')), 'r'
    ) as etl_config:
        config = yaml.load(etl_config, Loader=yaml.FullLoader)
        asyncio.run(async_main(config))

