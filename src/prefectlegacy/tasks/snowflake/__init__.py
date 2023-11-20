"""
This module contains a collection of tasks for interacting with snowflake databases via
the snowflake-connector-python library.
"""

try:
    from prefectlegacy.tasks.snowflake.snowflake import (
        SnowflakeQuery,
        SnowflakeQueriesFromFile,
    )
except ImportError as err:
    raise ImportError(
        'Using `prefectlegacy.tasks.snowflake` requires Prefect to be installed with the "snowflake" extra.'
    ) from err

__all__ = ["SnowflakeQueriesFromFile", "SnowflakeQuery"]