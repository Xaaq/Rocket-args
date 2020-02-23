You want to contribute? Great!

Below you will find instructions how to setup environment, launch tests, build docs etc.

## Setup environment

Before you start install [pyenv]https://github.com/pyenv/pyenv) if you haven't yet - it is tool for managing python
versions.

1. Clone repo.
1. Install appropriate python versions supported by this repository by `pyenv`:

    ```
    $ pyenv install 3.8.0 && pyenv install 3.7.5 && pyenv install 3.6.9
    ```

1. Make `pyenv` automatically use those versions - it will use first version and fallback to next ones when there is
    need (what will be used when launching `tox`):

    ```
    $ pyenv local 3.8.0 3.7.5 3.6.9
    ```

1. Install [poetry](https://python-poetry.org/) - tool for dependency managing, building and deploying packages:

    ```
    $ pip install poetry
    ```

1. Make poetry install all needed packages (from `pyproject.toml`) and create virtualenv for you:

    ```
    $ poetry install
    ```

1. Go inside virtualenv created by `poetry`:

    ```
    $ poetry shell
    ```

    !!! note
        If you will exit shell and open it afresh make sure to execute this command again - otherwise installed python
        packages probably won't be available.

1. `poetry` have already installed [pre-commit](https://pre-commit.com/) for you - we use it to run various formatters
    automatically on every commit. To turn on (install) `pre-commit` in this repository type:

    ```
    $ pre-commit install
    ```

## Running tests

You can run tests either against you actual python version - faster version (good for fast checking if our changes
didn't break anything):
```
$ pytest tests
```

or run them against all supported python versions using [tox](https://tox.readthedocs.io/en/latest/) - slower version
(good for final check if everything we've done works):
```
$ tox
```

## Building and running docs

To build and live-preview docs use following [mkdocs](https://www.mkdocs.org/) command:
```
$ mkdocs serve
```
and then paste link outputted by this command to web browser.

## Using Makefile

Instead of having to remember all commands to run tests, lint, checks etc. you can use `make` command to execute them.
All aliases are specified in `Makefile`.

You can also type `make` to list them:
```
$ make
help                 show this message
clean                remove all build and test artifacts along with python cache
type-check           check code for typing errors
lint                 check code style with flake8
coverage             check code coverage
test                 run fast tests using pytest
test-all             run tests against different python versions using tox
test-all-fast        run tests against different python versions using tox in parallel
docs                 build docs and launch them with live-reload
dist                 builds source and wheel package
```

Now to use any of these commands type `make <command name>`. For example:

* `make lint` ro run linter,
* `make test` to run tests,
* `make docs` to build and reload docs.
