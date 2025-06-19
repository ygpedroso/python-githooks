import os
import sys
import pathlib
from .helpers import create_config_file, create_git_hooks

__BASE_DIR__ = pathlib.Path.cwd()
__GITHOOKS_BASE_DIR__ = __BASE_DIR__ / ".git" / "hooks"
__GITHOOKS_CONFIGFILE_YAML_PATH__ = __BASE_DIR__ / ".githooks.yml"
__GITHOOKS_CONFIGFILE_YML_PATH__ = __BASE_DIR__ / ".githooks.yaml"


def get_config_file_path():
    """Returns the path to the config file, prioritizing .yml over .yaml"""
    if __GITHOOKS_CONFIGFILE_YAML_PATH__.is_file():
        return __GITHOOKS_CONFIGFILE_YAML_PATH__
    if __GITHOOKS_CONFIGFILE_YML_PATH__.is_file():
        return __GITHOOKS_CONFIGFILE_YML_PATH__
    # If neither exists, default to .yml for creation
    return __GITHOOKS_CONFIGFILE_YAML_PATH__


def main():
    if __GITHOOKS_BASE_DIR__.is_dir():
        configfile_path = get_config_file_path()
        if not configfile_path.is_file():
            create_config_file(configfile_path=configfile_path)
        create_git_hooks(configfile_path=configfile_path, githooks_dir=__GITHOOKS_BASE_DIR__)
    else:
        message = '''
        Sorry, this is not a GIT repository.
        Please, run 'git init' before trying to install the hooks.
        '''
        print(message)
        sys.exit(1)


if __name__ == '__main__':
    main()
