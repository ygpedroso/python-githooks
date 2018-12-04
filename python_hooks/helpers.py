import os
import sys
import stat
from configparser import ConfigParser
from .hook_template import hook_template


def create_config_file(configfile_path):
    config = ConfigParser()
    config['pre-commit'] = {'command': 'echo Pre commit hook installed. Replace this line with your own command'}
    with open(configfile_path, 'w') as configfile:
        config.write(configfile)


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
                    file.write(hook_template.format(section=section, command=command).encode())
                    st = os.stat(githook_file)
                    os.chmod(githook_file, st.st_mode | stat.S_IEXEC)
                print('{} hook successfully created for running "{}"'.format(section, command))
    else:
        message = '''
        Unable to find the ".githooks" configuration file.
        Please, create it and try again.
        '''
        print(message)
        sys.exit(1)
