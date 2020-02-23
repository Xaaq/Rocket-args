<p align="center">
    <img src="https://i.imgur.com/vjEOvJj.png" alt="logo">
    <b>Make your arg parsing even more declarative!</b><br>
</p>

<p align="center">
    <a href="https://travis-ci.com/Xaaq/Rocket-args">
        <img src="https://travis-ci.com/Xaaq/Rocket-args.svg?branch=master" alt="badge">
    </a>
    <a href="https://pypi.org/project/rocket-args/">
        <img src="https://img.shields.io/badge/pypi-0.1.0-informational" alt="badge">
    </a>
    <a href="https://github.com/Xaaq/Rocket-args/blob/master/LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-informational" alt="badge">
    </a>
</p>

---

**Source code**:
<a href="https://github.com/Xaaq/Rocket-args">
    https://github.com/Xaaq/Rocket-args
</a>

**Documentation**:
<a href="https://xaaq.github.io/Rocket-args">
    https://xaaq.github.io/Rocket-args
</a>

---

## Overview

So you wanted a tool that handles parsing arguments? You've come to right place!

Key features:

* fully declarative,
* less boilerplate code required,
* type hints,
* IDE auto-completion - no more strange `Namespace` objects.

## Installation

You will need Python 3.6+

In order to install it:
```
pip install rocket-args
```

## Examples

### Simple CLI args

Create `main.py` with following content:
```python
from rocket_args import RocketBase

class MyArgs(RocketBase):
    my_int: int
    my_float: float
    my_str: str

args = MyArgs.parse_args()
print(args)
```

Call it with arguments:
```
$ python main.py --my-int 1234 --my-float 12.34 --my-string abcd
MyArgs(my_int=1234, my_float=12.34, my_str=abcd)
```

### Default values

You can make CLI arg optional and provide its default value:
```python
from rocket_args import RocketBase

class MyArgs(RocketBase):
    my_int: int = 1234
    my_float: float = 12.34
    my_str: str = "abcd"

args = MyArgs.parse_args()
print(args)
```

Call it without arguments:
```
$ python main.py
MyArgs(my_int=1234, my_float=12.34, my_str=abcd)
```

### CLI arguments with additional metadata

Use `Argument` to provide additional metadata for generated arguments:
```python
from rocket_args import RocketBase, Argument

class MyArgs(RocketBase):
    my_int: int = Argument(names=["-i", "--my-int-arg"], default=1234, help="my int argument")
    my_float: float = Argument(names=["-f", "--my-float-arg"], default=12.34, help="my float argument")
    my_str: str = Argument(names=["-s", "--my-str-arg"], default="abcd", help="my str argument")

args = MyArgs.parse_args()
print(args)
```

Call it using specified names (or let if fallback to default):
```
$ python main.py -i 5678 --my-float-arg 56.78
MyArgs(my_int=5678, my_float=56.78, my_str=abcd)
```

### Auto-generated help

```
$ python main.py --help
usage: main.py [-h] [-i MY_INT_ARG] [-f MY_FLOAT_ARG] [-s MY_STR_ARG]

optional arguments:
  -h, --help            show this help message and exit
  -i MY_INT_ARG, --my-int-arg MY_INT_ARG
                        my int argument
  -f MY_FLOAT_ARG, --my-float-arg MY_FLOAT_ARG
                        my float argument
  -s MY_STR_ARG, --my-str-arg MY_STR_ARG
                        my str argument
```
