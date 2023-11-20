"""
A collection of tasks for running Jupyter notebooks.
"""
try:
    from prefectlegacy.tasks.jupyter.jupyter import ExecuteNotebook
except ImportError as import_error:
    raise ImportError(
        'Using `prefectlegacy.tasks.jupyter` requires Prefect to be installed with the "jupyter" extra.'
    ) from import_error

__all__ = ["ExecuteNotebook"]