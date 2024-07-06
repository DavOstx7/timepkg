import time
from functools import wraps
from dataclasses import dataclass, astuple, asdict
from typing import TypeVar, Callable

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

Parameters = ParamSpec("Parameters")
ReturnType = TypeVar("ReturnType")


@dataclass
class KeeperResult:
    return_value: ReturnType
    execution_time: float

    def tuple(self) -> tuple:
        return astuple(self)

    def dict(self) -> dict:
        return asdict(self)

    def __iter__(self):
        yield self.return_value
        yield self.execution_time


Function = Callable[..., ReturnType]
KeeperWrapper = Callable[..., KeeperResult]


def timekeeper(function: Function) -> KeeperWrapper:
    @wraps(function)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> KeeperResult:
        start_time = time.perf_counter()
        return_value = function(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return KeeperResult(return_value=return_value, execution_time=execution_time)

    return wrapper
