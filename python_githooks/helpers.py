import os
import sys
import stat
import subprocess
from configparser import ConfigParser


def create_config_file(configfile_path):
    config = ConfigParser()
    config['pre-commit'] = {'command': 'echo Pre commit hook installed. Replace this line with your own command'}
    with open(configfile_path, 'w') as configfile:
        config.write(configfile)


def _unable_to_find_config():
        message = '''
        Unable to find the ".githooks.ini" configuration file.
        Please, create it and try again.
        '''
        print(message)
        sys.exit(1)


def create_git_hooks(configfile_path, githooks_dir):
    config = ConfigParser()
    if os.path.isfile(configfile_path):
        config.read(configfile_path)
        for section in config.sections():
            hook = config[section]
            if 'command' in hook:
                command = hook['command']
                githook_file = os.path.join(githooks_dir, section)
                with open(githook_file, 'wb') as file:
                    file.write('githooks {}'.format(section).encode())
                    st = os.stat(githook_file)
                    os.chmod(githook_file, st.st_mode | stat.S_IEXEC)
                print('{} hook successfully created for running "{}"'.format(section, command))
    else:
        _unable_to_find_config()


def execute_git_hook(section, configfile_path):
    print('python-githooks > {}'.format(section))
    config = ConfigParser()
    if os.path.isfile(configfile_path):
        config.read(configfile_path)
        if config.has_option(section, 'command'):
            command = config[section]['command']
            sys.exit(subprocess.call(command, shell=True))
    else:
        _unable_to_find_config()
