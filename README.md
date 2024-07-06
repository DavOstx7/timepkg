# timepkg

The official repository fof the timepkg python package!

## Installation

```shell
pip install timepkg
```

## Usage

### Timekeeper

```python
import time
from timepkg import timekeeper


@timekeeper
def function():
    print("Hello World!")
    ...
    time.sleep(1)
    return "Goodbye!"


result = function()
print(result)
return_value, execution_time = function()
print(return_value, execution_time)
```

```bash
Hello World!
KeeperResult(return_value='Goodbye!', execution_time=1.0127643000000002)
Hello World!
Goodbye! 1.0116009
```

### Guardian

```python
import time
from timepkg import guardian


@guardian(save_metadata=True, guarded_exceptions=[ValueError])
def function():
    print("Hello World!")
    ...
    time.sleep(1)
    raise ValueError("Error!")


result = function()
print(result)
return_value, execution_time, (start_time, end_time, raised_exception) = function()
print(return_value, execution_time, start_time, end_time, raised_exception)
```

```bash
Hello World!
GuardianResult(return_value=None, execution_time=1.00541090965271, metadata=GuardianMetadata(start_time=1720282040.3592346, end_time=1720282041.3646455, raised_exception=ValueError('Error!',)))
Hello World!
None 1.0010006427764893 1720282041.3646455 1720282042.3656461 Error!
```

