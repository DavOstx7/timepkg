import pytest

import time
from tests.conftest import VALID_EXECUTION_ERROR_MARGIN, VALID_TIMESTAMPING_ERROR_MARGIN, FUNCTION_EXIT_OVERHEAD
from timepkg.guardian import guardian, GuardianResult, GuardianMetadata
from timepkg.validation import is_valid_time_margin


def test_metadata_creation(positive_float_factory):
    start_time, end_time, raised_exception = positive_float_factory(), positive_float_factory(), None
    metadata = GuardianMetadata(start_time=start_time, end_time=end_time, raised_exception=raised_exception)

    assert metadata.start_time == start_time
    assert metadata.end_time == end_time
    assert metadata.raised_exception == raised_exception


def test_metadata_casting(positive_float_factory):
    start_time, end_time, raised_exception = positive_float_factory(), positive_float_factory(), None
    metadata = GuardianMetadata(start_time=start_time, end_time=end_time, raised_exception=raised_exception)

    assert metadata.tuple() == (start_time, end_time, raised_exception)
    assert metadata.dict() == {"start_time": start_time, "end_time": end_time, "raised_exception": raised_exception}


def test_result_creation(value_factory, positive_float_factory):
    return_value, execution_time, metadata = value_factory(), positive_float_factory(), None
    result = GuardianResult(return_value=return_value, execution_time=execution_time, metadata=metadata)

    assert result.return_value == return_value
    assert result.execution_time == execution_time
    assert result.metadata == metadata


def test_result_casting(value_factory, positive_float_factory):
    return_value, execution_time, metadata = value_factory(), positive_float_factory(), None
    result = GuardianResult(return_value=return_value, execution_time=execution_time, metadata=metadata)

    assert result.tuple() == (return_value, execution_time, metadata)
    assert result.dict() == {"return_value": return_value, "execution_time": execution_time, "metadata": metadata}


def test_saving_metadata(value_factory, testable_duration_factory):
    return_value, execution_time = value_factory(), testable_duration_factory()

    start_time = time.time()

    @guardian(save_metadata=True, guarded_exceptions=None)
    def dummy_function():
        time.sleep(execution_time)
        return return_value

    end_time = time.time()

    result = dummy_function()

    assert result.return_value == return_value
    assert is_valid_time_margin(execution_time, result.execution_time, VALID_EXECUTION_ERROR_MARGIN)
    assert is_valid_time_margin(start_time, result.metadata.start_time, VALID_TIMESTAMPING_ERROR_MARGIN)
    assert is_valid_time_margin(
        end_time, result.metadata.end_time, VALID_TIMESTAMPING_ERROR_MARGIN + FUNCTION_EXIT_OVERHEAD
    )
    assert result.metadata.raised_exception is None


def test_not_saving_metadata(testable_duration_factory):
    execution_time = testable_duration_factory()
    _args = (1, 2, 3)
    _kwargs = {"d": 4, "e": 5, "f": 6}

    @guardian(save_metadata=False, guarded_exceptions=None)
    def dummy_function(*args, **kwargs):
        time.sleep(execution_time)
        return args, kwargs

    result = dummy_function(*_args, **_kwargs)

    assert result.return_value == (_args, _kwargs)
    assert is_valid_time_margin(execution_time, result.execution_time, VALID_EXECUTION_ERROR_MARGIN)
    assert result.metadata is None


def test_raising_exception_with_exception_guard(exception_type_factory):
    exception_type = exception_type_factory()
    exception_object = exception_type()

    @guardian(save_metadata=True, guarded_exceptions=(exception_type,))
    def dummy_function():
        raise exception_object

    result = dummy_function()
    assert exception_object == result.metadata.raised_exception


def test_raising_exception_with_wrong_exception_guard(exception_type_factory):
    exception_type = exception_type_factory()

    class DummyError(Exception):
        pass

    @guardian(save_metadata=True, guarded_exceptions=(exception_type,))
    def dummy_function():
        raise DummyError()

    with pytest.raises(DummyError):
        dummy_function()


def test_raising_exception_without_exception_guard(exception_type_factory):
    exception_type = exception_type_factory()
    exception_object = exception_type()

    @guardian(save_metadata=True, guarded_exceptions=None)
    def dummy_function():
        raise exception_object

    with pytest.raises(exception_type):
        dummy_function()
