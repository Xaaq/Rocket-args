<div align="center">
    <img src="https://i.imgur.com/vjEOvJj.png" alt="logo">
    <b>Make your arg parsing even more declarative!</b>
</div>

---

<div align="center">
    <a href="https://github.com/Xaaq/Rocket-args/blob/complete-documentation/LICENSE">
        <img src="https://img.shields.io/badge/license-MIT-informational" alt="badge">
    </a>
</div>

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
* no more `Namespace` objects with no IDE auto-completion!

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

### Auto-generated help

```
$ python main.py --help
usage: main.py [-h] [--my-int MY_INT] [--my-float MY_FLOAT] [--my-str MY_STR]

optional arguments:
  -h, --help           show this help message and exit
  --my-int MY_INT
  --my-float MY_FLOAT
  --my-str MY_STR
```

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
