## Default CLI argument names

By default, for every class field there will be generated CLI argument following these steps:

1. All underscores will be changed to dashes.
1. Two leading dashes will be added.

For example:

* field `arg` -> CLI argument `--arg`
* field `long_arg_name` -> CLI argument `--long-arg-name`

## Explicit CLI argument names

You can explicitly specify which names should be generated for arguments using `Argument`:
```python
from rocket_args import RocketBase, Argument

class MyArgs(RocketBase):
    arg: str = Argument(names=["-a", "--argument"])

args = MyArgs.parse_args()
print(args)
```

Now you can use any of these names in CLI:
```
$ python main.py -a abc
MyArgs(arg=abc)
$ python main.py --argument abc
MyArgs(arg=abc)
```

If you specify argument names like above, then default argument names won't be generated:
```
$ python main.py --arg abc
usage: main.py [-h] -a ARGUMENT
scratch.py: error: the following arguments are required: -a/--argument
```

## Default values

When using `Argument` you can set default values for your arguments in the other way. So this:
```python
from rocket_args import RocketBase, Argument

class MyArgs(RocketBase):
    my_int: int = Argument(default=123)
    my_float: float = Argument(default=12.34)
    my_str: str = Argument(default="abcd")
```

is equivalent to that:
```python
from rocket_args import RocketBase

class MyArgs(RocketBase):
    my_int: int = 123
    my_float: float = 12.34
    my_str: str = "abcd"
```

## Help message

You can also specify help message:
```python
from rocket_args import RocketBase, Argument

class MyArgs(RocketBase):
    my_int: int = Argument(help="my int argument")
    my_float: float = Argument(help="my float argument")
    my_str: str = Argument(help="my str argument")

args = MyArgs.parse_args()
print(args)
```

When launched from command line:
```
$ python main.py --help
usage: main.py [-h] --my-int MY_INT --my-float MY_FLOAT --my-str MY_STR

optional arguments:
  -h, --help           show this help message and exit
  --my-int MY_INT      my int argument
  --my-float MY_FLOAT  my float argument
  --my-str MY_STR      my str argument
```
