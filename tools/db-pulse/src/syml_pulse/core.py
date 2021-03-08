import textwrap
from asyncio import sleep
from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import text, select, column, or_, and_

stats_columns = [
    column('table_schema'),
    column('table_name'),
    column('row_estimate'),
    column('total_bytes'),
    column('index_bytes'),
    column('toast_bytes'),
]


@dataclass
class TableStats:
    row_estimate: int
    total_bytes: int
    index_bytes: int
    toast_bytes: int


@dataclass
class TableStatsDifference:
    source_schema: str
    destination_schema: str
    source_table: str
    destination_table: str

    source_stats: TableStats
    destination_stats: TableStats
    difference: TableStats


async def get_current_data_for_schemas(
    conn,
    schemas: Iterable = None,
    tables: Iterable = None,
):
    query = text(textwrap.dedent(
        """
        SELECT c.oid
           , nspname                               AS table_schema
           , relname                               AS table_name
           , c.reltuples                           AS row_estimate
           , pg_total_relation_size(c.oid)         AS total_bytes
           , pg_indexes_size(c.oid)                AS index_bytes
           , pg_total_relation_size(reltoastrelid) AS toast_bytes
        FROM pg_class c
               LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE relkind = 'r'
        """
    )).columns(*stats_columns)

    query = select(stats_columns).select_from(query)

    if schemas:
        query = query.where(column('table_schema').in_(schemas))
    elif tables:
        query = query.where(or_(*[
            and_(
                column('table_schema') == ct.get('schema'),
                column('table_name') == ct.get('table'),
            )
            for ct in tables
        ]))

    async_result = await conn.stream(query)

    async for row in async_result:
        yield row


async def compare_source_dest(
    conn, mappings: Iterable
):
    stats = {
        (r.table_schema, r.table_name): r
        async for r in get_current_data_for_schemas(
            conn,
            tables=(
                table for mapping in mappings for table in mapping.values()
            )
        )}

    for mapping in mappings:
        source = mapping.get('source')
        destination = mapping.get('destination')

        source_stats = stats.get((source['schema'], source['table']))
        destination_stats = stats.get(
            (destination['schema'], destination['table'])
        )

        yield TableStatsDifference(
            source_schema=source['schema'],
            destination_schema=destination['schema'],
            source_table=source['table'],
            destination_table=destination['table'],
            source_stats=TableStats(
                row_estimate=source_stats.row_estimate,
                total_bytes=source_stats.total_bytes,
                index_bytes=source_stats.index_bytes,
                toast_bytes=source_stats.toast_bytes,
            ),
            destination_stats=TableStats(
                row_estimate=destination_stats.row_estimate,
                total_bytes=destination_stats.total_bytes,
                index_bytes=destination_stats.index_bytes,
                toast_bytes=destination_stats.toast_bytes

            ),
            difference=TableStats(
                row_estimate=source_stats.row_estimate - destination_stats.row_estimate,
                total_bytes=source_stats.total_bytes - destination_stats.total_bytes,
                index_bytes=source_stats.index_bytes - destination_stats.index_bytes,
                toast_bytes=source_stats.toast_bytes - destination_stats.toast_bytes,
            )
        )


async def watch_source_dest(
    conn, mappings: Iterable,
):

    latest_stats = dict()

    while True:
        async for diff in compare_source_dest(conn, mappings):
            key = diff.source_schema, diff.source_table
            stats = latest_stats.get(key)

            if stats:
                if stats.difference.total_bytes != diff.difference.total_bytes:
                    yield diff
            else:
                yield diff

            latest_stats[key] = diff

        await sleep(5)
