import asyncio
import logging
from os import getenv
from pathlib import Path

import humanize
import yaml
from sqlalchemy.ext.asyncio import create_async_engine

from src.syml_pulse.core import compare_source_dest, watch_source_dest

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
            if diff.difference.total_bytes < 0:
                print('- source {:70} ({:10} ~{:10} rows) SMALLER by {:10} - {:.2f}%'.format(
                    diff.source_table,
                    humanize.naturalsize(abs(diff.source_stats.total_bytes)),
                    int(diff.source_stats.row_estimate),
                    humanize.naturalsize(abs(diff.difference.total_bytes)),
                    abs(diff.difference.total_bytes / diff.source_stats.total_bytes * 100)
                    if diff.source_stats.total_bytes > 0 else '∞'
                ))
            else:
                print('- source {:70} ({:10} ~{:10} rows) LARGER by {:10} - {:.2f}%'.format(
                    diff.source_table,
                    humanize.naturalsize(abs(diff.source_stats.total_bytes)),
                    int(diff.source_stats.row_estimate),
                    humanize.naturalsize(abs(diff.difference.total_bytes)),
                    abs(diff.difference.total_bytes / diff.source_stats.total_bytes * 100)
                    if diff.source_stats.total_bytes > 0 else '∞'
                ))


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.INFO)

    with open(
        str(Path('../examples/elt-progress/simple.etl.syml.yaml')), 'r'
    ) as etl_config:
        config = yaml.load(etl_config, Loader=yaml.FullLoader)
        asyncio.run(async_main(config))
