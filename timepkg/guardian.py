import time
from functools import wraps
from dataclasses import dataclass, astuple, asdict
from typing import Callable, Optional, Iterable
from timepkg.keeper import KeeperResult, Function, Parameters

NO_GUARDED_EXCEPTIONS = ()


@dataclass
class GuardianMetadata:
    start_time: float
    end_time: float
    raised_exception: Optional[Exception]

    def tuple(self) -> tuple:
        return astuple(self)

    def dict(self) -> dict:
        return asdict(self)

    def __iter__(self):
        yield self.start_time
        yield self.end_time
        yield self.raised_exception


@dataclass
class GuardianResult(KeeperResult):
    metadata: Optional[GuardianMetadata]

    def __iter__(self):
        yield from super().__iter__()
        yield self.metadata


GuardianWrapper = Callable[..., GuardianResult]
GuardianDecorator = Callable[[Function], GuardianWrapper]


def guardian(save_metadata: bool = True, guarded_exceptions: Optional[Iterable[Exception]] = None) -> GuardianDecorator:
    if not guarded_exceptions:
        guarded_exceptions = NO_GUARDED_EXCEPTIONS

    def decorator(function: Function) -> GuardianWrapper:
        @wraps(function)
        def wrapper(*args: Parameters.args, **kwargs: Parameters.kwargs) -> GuardianResult:
            return_value = None
            raised_exception = None
            metadata = None

            start_time = time.time()
            try:
                return_value = function(*args, **kwargs)
            except (*guarded_exceptions,) as exc:
                raised_exception = exc
            end_time = time.time()
            execution_time = end_time - start_time

            if save_metadata:
                metadata = GuardianMetadata(start_time=start_time, end_time=end_time, raised_exception=raised_exception)

            return GuardianResult(return_value=return_value, execution_time=execution_time, metadata=metadata)

        return wrapper

    return decorator
