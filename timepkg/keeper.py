import time
from functools import wraps
from dataclasses import dataclass
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


Function = TypeVar("Function", bound=Callable[Parameters, ReturnType])
KeeperFunction = TypeVar("KeeperFunction", bound=Callable[Parameters, KeeperResult])


def timekeeper(function: Function) -> KeeperFunction:
    @wraps(function)
    def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> KeeperResult:
        start_time = time.perf_counter()
        return_value = function(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return KeeperResult(return_value=return_value, execution_time=execution_time)

    return wrapper
