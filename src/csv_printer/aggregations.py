from datetime import date
from statistics import mean
from typing import Callable, Sequence

ALLOWED_TYPES = float | int | date
ALLOWED_LISTS = Sequence[float] | Sequence[int] | Sequence[date]


def calculate(
    aggregator: Callable[[ALLOWED_LISTS], ALLOWED_TYPES],
    values: ALLOWED_LISTS
) -> ALLOWED_TYPES:
    assert callable(aggregator)
    assert isinstance(values, list)
    assert values
    assert isinstance(values[0], (
        float, int, date
    )), type([values[0]])
    agg = aggregator
    value0 = values[0]
    if isinstance(value0, int):
        assert all((isinstance(i, int) for i in values))
        return round(agg(values), ndigits=2)
    if isinstance(value0, float):
        assert all((isinstance(i, float) for i in values))
        return round(agg(values), ndigits=2)
    if isinstance(value0, date):
        assert all((isinstance(i, date) for i in values))
        return date.fromordinal(
            round(float(
                agg(
                    i.toordinal() for i in values  # type:ignore
                ) / len(values)
            ))
        )
    assert None, type(value0)


def _mean(values: ALLOWED_LISTS) -> ALLOWED_TYPES:
    return calculate(
        mean,  # type: ignore
        values
    )


def _min(values: ALLOWED_LISTS) -> ALLOWED_TYPES:
    return calculate(min, values)


def _max(values: ALLOWED_LISTS) -> ALLOWED_TYPES:
    return calculate(max, values)


OPERATIONS = {
    'average': _mean,
    'mean': _mean,
    'median': _mean,
    'min': _min,
    'max': _max
}
