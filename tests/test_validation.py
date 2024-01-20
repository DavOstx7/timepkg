from timepkg.validation import valid_execution_time


def test_valid_execution_time():
    assert valid_execution_time(expected_time=10, actual_time=11, error_margin=2)
    assert valid_execution_time(expected_time=10, actual_time=9, error_margin=2)

    assert valid_execution_time(expected_time=1, actual_time=1.1, error_margin=0.1)
    assert valid_execution_time(expected_time=1, actual_time=0.9, error_margin=0.1)


def test_invalid_execution_time():
    assert not valid_execution_time(expected_time=10, actual_time=11, error_margin=0.5)
    assert not valid_execution_time(expected_time=10, actual_time=9, error_margin=0.5)

    assert not valid_execution_time(expected_time=1, actual_time=1.1, error_margin=0.09)
    assert not valid_execution_time(expected_time=1, actual_time=0.9, error_margin=0.09)
