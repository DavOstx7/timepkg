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


result = function()
print(result)
```

```bash
Hello World!
KeeperResult(return_value=None, execution_time=1.0116821)
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
```

```bash
Hello World!
GuardianResult(return_value=None, execution_time=1.0120351314544678, metadata=GuardianMetadata(start_time=1705785487.1720371, end_time=1705785488.1840723, raised_exception=ValueError('Error!',)))
```

