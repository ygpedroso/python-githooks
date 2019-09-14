# python-githooks

[![code linting: flake8](https://img.shields.io/badge/lint-flake8-blue.svg)](http://flake8.pycqa.org/)  [![code quality: pytest](https://img.shields.io/badge/test-pytest-yellow.svg)](https://docs.pytest.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![CircleCI](https://circleci.com/gh/ygpedroso/python-githooks.svg?style=svg)](https://circleci.com/gh/ygpedroso/python-githooks)

> Create git hooks with ease using a simple configuration file in a git project

## Install

```bash
pip install python-githooks
```

## Usage

1. Create a `.githooks.ini` configuration file(If not provided a dummy configuration file will be created).
2. Add sections based on `git hooks names`  followed by a `command` property with the shell code you want to run.
3. Run either `python -m python_githooks` or `githooks` in your virtual environment.

**Configuration file example**:

```ini
# .githooks.ini

[pre-commit]
command = pytest --cov

[pre-push]
command = pytest --cov && flake8
```

* Remember to re-run `python -m python_githooks` or `githooks` when you add new hooks.

## Removing a hook

If you already created a hook and now want to remove it, just set the command value to empty, like this:

```ini
# .githooks.ini

[pre-commit]
command =
```

This will not actually physically remove the hook from the git local project, just will make it instantly exit with `0` status code.

## License

python-githooks is [MIT-licensed](https://github.com/ygpedroso/python-githooks/blob/master/LICENSE).
