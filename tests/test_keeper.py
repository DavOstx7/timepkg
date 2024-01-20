import time
from tests.conftest import VALID_EXECUTION_ERROR_MARGIN
from timepkg.keeper import timekeeper, KeeperResult
from timepkg.validation import valid_time_margin


def test_result_creation(value_factory, positive_float_factory):
    return_value, execution_time = value_factory(), positive_float_factory()
    result = KeeperResult(return_value=return_value, execution_time=execution_time)

    assert result.return_value == return_value
    assert result.execution_time == execution_time


def test_result_casting(value_factory, positive_float_factory):
    return_value, execution_time = value_factory(), positive_float_factory()
    result = KeeperResult(return_value=return_value, execution_time=execution_time)

    assert result.tuple() == (return_value, execution_time)
    assert result.dict() == {"return_value": return_value, "execution_time": execution_time}


def test_parameterless_function(value_factory, testable_duration_factory):
    return_value, execution_time = value_factory(), testable_duration_factory()

    @timekeeper
    def dummy_function():
        time.sleep(execution_time)
        return return_value

    result = dummy_function()

    assert result.return_value == return_value
    assert valid_time_margin(execution_time, result.execution_time, VALID_EXECUTION_ERROR_MARGIN)


def test_parameterized_function(testable_duration_factory):
    execution_time = testable_duration_factory()
    _args = (1, 2, 3)
    _kwargs = {"d": 4, "e": 5, "f": 6}

    @timekeeper
    def dummy_function(*args, **kwargs):
        time.sleep(execution_time)
        return args, kwargs

    result = dummy_function(*_args, **_kwargs)

    assert result.return_value == (_args, _kwargs)
    assert valid_time_margin(execution_time, result.execution_time, VALID_EXECUTION_ERROR_MARGIN)
