import pytest

from timepkg.validation import is_valid_time_margin


@pytest.mark.parametrize("et, at,  em", [
    (10, 11, 2),
    (10, 9, 2),
    (1, 1.1, 0.1),
    (1, 0.9, 0.1),
])
def test_valid_time_margin(et, at, em):
    assert is_valid_time_margin(expected_time=et, actual_time=at, error_margin=em)


@pytest.mark.parametrize("et, at,  em", [
    (10, 11, 0.5),
    (10, 9, 0.5),
    (1, 1.1, 0.09),
    (1, 0.9, 0.09),
])
def test_invalid_time_margin(et, at, em):
    assert not is_valid_time_margin(expected_time=et, actual_time=at, error_margin=em)
