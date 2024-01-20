import pytest
import random
from typing import Callable, Any, Type

MIN_TESTABLE_DURATION = 0
MAX_TESTABLE_DURATION = 0.5
VALID_EXECUTION_ERROR_MARGIN = 0.1
VALID_TIMESTAMPING_ERROR_MARGIN = 0.1
FUNCTION_EXIT_OVERHEAD = 0.2


@pytest.fixture
def value_factory() -> Callable[..., Any]:
    return lambda: random.choice(["123", "-123", 123, -123, 123.0, -123.0, True, False])


@pytest.fixture
def positive_float_factory() -> Callable[..., float]:
    return lambda: random.uniform(1, 100)


@pytest.fixture
def testable_duration_factory() -> Callable[..., float]:
    return lambda: random.uniform(MIN_TESTABLE_DURATION, MAX_TESTABLE_DURATION)


@pytest.fixture
def exception_type_factory() -> Callable[..., Type[Exception]]:
    return lambda: random.choice([ValueError, TypeError, SyntaxError, IndexError])
