from typing import Any


def create_batches_list(data: list[Any], batch_size: int) -> list[list]:
    """
    Create batches list from given list of data.

    Parameters
    ----------
    data: list[Any]
        data which should be batched
    batch_size: int
        size of each unit batch


    Returns
    -------
    list[list[Any]]
        batches list
    """
    return [data[idx : idx + batch_size] for idx in range(0, len(data), batch_size)]
