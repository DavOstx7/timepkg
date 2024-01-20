from dataclasses import dataclass
from typing import TypeVar

ReturnType = TypeVar("ReturnType")


@dataclass
class KeeperResult:
    return_value: ReturnType
    execution_time: float
