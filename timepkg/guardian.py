import time
from functools import wraps
from dataclasses import dataclass
from typing import Callable, Optional
from timepkg.keeper import KeeperResult, Function, Parameters


@dataclass
class GuardianResult(KeeperResult):
    raised_exception: Optional[Exception]


GuardianWrapper = Callable[Parameters, GuardianResult]
GuardianDecorator = Callable[[Function], GuardianWrapper]


def guardian(catch_exceptions: bool = False) -> GuardianDecorator:
    def decorator(function: Function) -> GuardianWrapper:
        @wraps(function)
        def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> GuardianResult:
            start_time = time.perf_counter()
            return_value = None
            raised_exception = None

            if catch_exceptions:
                try:
                    return_value = function(*args, **kwargs)
                except Exception as exc:
                    raised_exception = exc
            else:
                return_value = function(*args, **kwargs)

            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return GuardianResult(
                return_value=return_value, execution_time=execution_time, raised_exception=raised_exception
            )

        return wrapper

    return decorator
