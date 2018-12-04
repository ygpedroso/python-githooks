import os
from configparser import ConfigParser
from python_hooks.helpers import create_config_file


def test_config_file_creation(workspace_without_git):
    """create_config_file helper function should create file"""
    configfile_path = os.path.join(workspace_without_git, '.githooks.ini')
    create_config_file(configfile_path=configfile_path)
    assert os.path.isfile(configfile_path)


def test_config_file_default_values(workspace_without_git):
    """create_config_file helper function should create file with defaults values"""
    configfile_path = os.path.join(workspace_without_git, '.githooks.ini')
    create_config_file(configfile_path=configfile_path)
    config = ConfigParser()
    config.read(configfile_path)
    assert config.sections() == ['pre-commit']
    assert config['pre-commit']['command'] == 'echo Pre commit hook installed. Replace this line with your own command'
