import time
from functools import wraps
from dataclasses import dataclass, astuple, asdict
from typing import Callable, Optional
from timepkg.keeper import KeeperResult, Function, Parameters


@dataclass
class GuardianMetadata:
    start_time: float
    end_time: float
    raised_exception: Optional[Exception]

    def tuple(self) -> tuple:
        return astuple(self)

    def dict(self) -> dict:
        return asdict(self)


@dataclass
class GuardianResult(KeeperResult):
    metadata: Optional[GuardianMetadata]


GuardianWrapper = Callable[..., GuardianResult]
GuardianDecorator = Callable[[Function], GuardianWrapper]


def guardian(catch_exceptions: bool = False, verbose: bool = False) -> GuardianDecorator:
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

            if verbose:
                metadata = GuardianMetadata(start_time=start_time, end_time=end_time, raised_exception=raised_exception)
            else:
                metadata = None

            return GuardianResult(return_value=return_value, execution_time=execution_time, metadata=metadata)

        return wrapper

    return decorator
