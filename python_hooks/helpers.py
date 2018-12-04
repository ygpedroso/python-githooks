from configparser import ConfigParser


def create_config_file(configfile_path):
    config = ConfigParser()
    config['pre-commit'] = {'command': 'echo Pre commit hook installed. Replace this line with your own command'}
    with open(configfile_path, 'w') as configfile:
        config.write(configfile)

