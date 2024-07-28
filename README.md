# timepkg

timepkg is a python package which allows you to measure performance and benchmark your functions. Additionally, it can
timestamp your function and ensure it exits gracefully!

## Installation

```shell
pip install timepkg
```

## Usage

### Timekeeper

Timekeeper is a simple decorator. It uses performance counter (high resolution clock) to measure execution time:

```python
import time
from timepkg import timekeeper


@timekeeper
def function():
    ...
    time.sleep(1)
    return "Goodbye"


result = function()
print(f"1) {result}")

return_value, execution_time = function()
print(f"2) {[return_value, execution_time]}")
```

```bash
1) KeeperResult(return_value='Goodbye', execution_time=1.0078486000000002)
2) ['Goodbye', 1.0087065000000002]
```

### Guardian

Guardian is a decorator, which extends the functionality of Timekeeper. It uses epoch timestamps (system clock)
to measure execution time and save metadata. It can also guard against specific exceptions and ensure graceful exit:

```python
import time
from timepkg import guardian


@guardian(save_metadata=True, guarded_exceptions=[ValueError])
def function():
    ...
    time.sleep(1)
    raise ValueError("Error!")


result = function()
print(f"1) {result}")

return_value, execution_time, (start_time, end_time, raised_exception) = function()
print(f"2) {[return_value, execution_time, start_time, end_time, raised_exception]}")
```

```bash
1) GuardianResult(return_value=None, execution_time=1.0060713291168213, metadata=GuardianMetadata(start_time=1721595459.6064517, end_time=1721595460.612523, raised_exception=ValueError('Error!',)))
2) [None, 1.0149073600769043, 1721595460.612523, 1721595461.6274304, ValueError('Error!',)]
```
