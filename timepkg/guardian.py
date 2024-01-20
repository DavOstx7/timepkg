import time
from functools import wraps
from dataclasses import dataclass
from typing import Callable
from timepkg.keeper import KeeperResult, Function, Parameters


@dataclass
class GuardianResult(KeeperResult):
    pass


GuardianWrapper = Callable[Parameters, GuardianResult]
GuardianDecorator = Callable[[Function], GuardianWrapper]


def guardian() -> GuardianDecorator:
    def decorator(function: Function) -> GuardianWrapper:
        @wraps(function)
        def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> GuardianResult:
            start_time = time.perf_counter()
            return_value = function(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            return GuardianResult(return_value=return_value, execution_time=execution_time)

        return wrapper

    return decorator
