import pytest
import random
from typing import Any


MIN_TESTABLE_DURATION = 0
MAX_TESTABLE_DURATION = 0.5
VALID_ERROR_MARGIN_TIME = 0.1


@pytest.fixture
def random_value() -> Any:
    return random.choice(["123", "-123", 123, -123, 123.0, -123.0, True, False])


@pytest.fixture
def random_positive_float() -> float:
    return random.uniform(1, 100)


@pytest.fixture
def random_testable_duration() -> float:
    return random.uniform(MIN_TESTABLE_DURATION, MAX_TESTABLE_DURATION)
