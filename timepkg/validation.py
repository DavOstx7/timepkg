def valid_time_margin(expected_time: float, actual_time: float, error_margin: float) -> bool:
    return actual_time - error_margin <= expected_time <= actual_time + error_margin
