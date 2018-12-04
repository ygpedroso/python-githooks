import os
import sys
from .helpers import create_config_file, create_git_hooks

__BASE_DIR__ = os.environ["PWD"]
__GITHOOKS_BASE_DIR__ = os.path.join(__BASE_DIR__, '.git/hooks')
__GITHOOKS_CONFIGFILE_PATH__ = os.path.join(__BASE_DIR__, '.githooks.ini')


def main():
    if os.path.isdir(__GITHOOKS_BASE_DIR__):
        if not os.path.isfile(__GITHOOKS_CONFIGFILE_PATH__):
            create_config_file(configfile_path=__GITHOOKS_CONFIGFILE_PATH__)
        create_git_hooks(configfile_path=__GITHOOKS_CONFIGFILE_PATH__, githooks_dir=__GITHOOKS_BASE_DIR__)
    else:
        message = '''
        Sorry, this is not a GIT repository.
        Please, run 'git init' before trying to install the hooks.
        '''
        print(message)
        sys.exit(1)


if __name__ == '__main__':
    main()
