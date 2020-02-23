## Basic usage

To parse command line arguments in the simplest possible way create class that is inheriting after `RocketBase`. Then
for every CLI argument that you want to add, create class field with appropriate type hint:
```python
class MyArgs(RocketBase):
    my_int: int  # for CLI argument --my-int
    my_float: float  # for CLI argument --my-float
    my_str: str  # for CLI argument --my-str
```

!!! note
    You **must** provide type hints for class fields so they can be correctly parsed.

Then what you need is to call `parse_args()` method on class (not instance!) to let all CLI parsing magic happen:
```python
args = MyArgs.parse_args()
```

Now you can access all fields defined above:
```python
print(args.my_int, args.my_float, args.my_str)
```

---

Put all above code into some file - let's say `main.py`:
```python
from rocket_args import RocketBase

class MyArgs(RocketBase):
    my_int: int
    my_float: float
    my_str: str

args = MyArgs.parse_args()
print(args.my_int, args.my_float, args.my_str)
```

And launch it with arguments:
```
$ python main.py --my-int 1234 --my-float 12.34 --my-str abcd
1234 12.34 abcd
```

Also, all arguments specified in class are required - when you don't provide any of them you will get following message:
```
$ python main.py
usage: scratch.py [-h] --my-int MY_INT --my-float MY_FLOAT --my-str MY_STR
scratch.py: error: the following arguments are required: --my-int, --my-float, --my-str
```

## Pretty-printing CLI arguments

To reduce amount of boilerplate code print your arguments instance directly:
```python
from rocket_args import RocketBase

class MyArgs(RocketBase):
    my_int: int
    my_float: float
    my_str: str

args = MyArgs.parse_args()
print(args)
```

Now launch it:
```
$ python main.py --my-int 1234 --my-float 12.34 --my-str abcd
MyArgs(my_int=1234, my_float=12.34, my_str=abcd)
```

## Default values

You can specify default values for your fields:
```python
from rocket_args import RocketBase

class MyArgs(RocketBase):
    my_int: int = 123
    my_float: float = 12.34
    my_str: str = "abcd"

args = MyArgs.parse_args()
print(args)
```

Every CLI argument whose class field has default value assigned doesn't have to be provided from command line. So
launching above script without arguments will work:
```
$ python main.py
MyArgs(my_int=1234, my_float=12.34, my_str=abcd)
```

Of course you can overwrite them by providing arguments from command line:
```
$ python main.py --my-int 5678 --my-float 56.78 --my-str efgh
MyArgs(my_int=5678, my_float=56.78, my_str=efgh)
```

## Help

When you launch above script with `--help` parameter you will get help message:
```
$ python main.py --help
usage: main.py [-h] [--my-int MY_INT] [--my-float MY_FLOAT] [--my-str MY_STR]

optional arguments:
  -h, --help           show this help message and exit
  --my-int MY_INT
  --my-float MY_FLOAT
  --my-str MY_STR
```

## Generated CLI argument names

For every class field there will be generated CLI argument following these steps:

1. All underscores will be changed to dashes.
1. Two leading dashes will be added.

For example:

* field `arg` -> CLI argument `--arg`
* field `long_arg_name` -> CLI argument `--long-arg-name`
