from timepkg.validation import is_valid_time_margin


def test_valid_time_margin():
    assert is_valid_time_margin(expected_time=10, actual_time=11, error_margin=2)
    assert is_valid_time_margin(expected_time=10, actual_time=9, error_margin=2)

    assert is_valid_time_margin(expected_time=1, actual_time=1.1, error_margin=0.1)
    assert is_valid_time_margin(expected_time=1, actual_time=0.9, error_margin=0.1)


def test_invalid_time_margin():
    assert not is_valid_time_margin(expected_time=10, actual_time=11, error_margin=0.5)
    assert not is_valid_time_margin(expected_time=10, actual_time=9, error_margin=0.5)

    assert not is_valid_time_margin(expected_time=1, actual_time=1.1, error_margin=0.09)
    assert not is_valid_time_margin(expected_time=1, actual_time=0.9, error_margin=0.09)
