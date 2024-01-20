import time
from tests.conftest import VALID_ERROR_MARGIN_TIME
from timepkg.keeper import timekeeper, KeeperResult
from timepkg.validation import valid_execution_time


def test_result_creation(random_value, random_positive_float):
    result = KeeperResult(return_value=random_value, execution_time=random_positive_float)

    assert result.return_value == random_value
    assert result.execution_time == random_positive_float


def test_result_casting(random_value, random_positive_float):
    result = KeeperResult(return_value=random_value, execution_time=random_positive_float)

    assert (random_value, random_positive_float) == result.tuple()
    assert {"return_value": random_value, "execution_time": random_positive_float} == result.dict()


def test_parameterless_function(random_value, random_testable_duration):
    @timekeeper
    def dummy_function():
        time.sleep(random_testable_duration)
        return random_value

    result = dummy_function()

    assert result.return_value == random_value
    assert valid_execution_time(random_testable_duration, result.execution_time, VALID_ERROR_MARGIN_TIME)


def test_parameterized_function(random_testable_duration):
    _args = (1, 2, 3)
    _kwargs = {"d": 4, "e": 5, "f": 6}

    @timekeeper
    def dummy_function(*args, **kwargs):
        time.sleep(random_testable_duration)
        return args, kwargs

    result = dummy_function(*_args, **_kwargs)

    assert result.return_value == (_args, _kwargs)
    assert valid_execution_time(random_testable_duration, result.execution_time, VALID_ERROR_MARGIN_TIME)
