# python-githooks

[![code linting: flake8](https://img.shields.io/badge/lint-flake8-blue.svg)](http://flake8.pycqa.org/)  [![code quality: pytest](https://img.shields.io/badge/test-pytest-yellow.svg)](https://docs.pytest.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![CircleCI](https://circleci.com/gh/ygpedroso/python-githooks.svg?style=svg)](https://circleci.com/gh/ygpedroso/python-githooks)

> Create git hooks with ease using a simple configuration file in a git project

## Install
```bash
pip install python-githooks
```

## Usage
1. Create a `.githooks.yml` (or `.githooks.yaml`) configuration file. If not provided, a dummy configuration file will be created.
2. Define hooks as top-level keys. Under each hook, use a `commands` key (plural) which takes a list of shell commands to be executed sequentially.
3. Run either `python -m python_githooks` or `githooks` in your virtual environment.
* Configuration file Example:
```yaml
# .githooks.yml

pre-commit:
  commands:
    - pytest --cov
    - flake8 .
    - echo "Pre-commit checks passed!"

pre-push:
  commands:
    - echo "Running pre-push checks..."
    - python manage.py test
```
* Remember to re-run `python -m python_githooks` or `githooks` every time you make changes to the configuration file,
whether it is for adding new hooks or modifying the current ones.

## Removing or Disabling a hook
If you want to effectively disable a hook (e.g., one that was previously defined), you can provide an empty list to the `commands` key:
```yaml
# .githooks.yml

pre-commit:
  commands: [] # This pre-commit hook will do nothing
```
This will make the hook instantly exit with a `0` status code. To completely remove a hook definition, simply delete its top-level key (e.g., `pre-commit:`) from the YAML file and re-run `githooks`. The corresponding hook script in `.git/hooks/` will then execute an empty list of commands.

## License
python-githooks is [MIT-licensed](https://github.com/ygpedroso/python-githooks/blob/master/LICENSE).
