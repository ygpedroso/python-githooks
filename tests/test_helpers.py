import os
from configparser import ConfigParser
from python_hooks.helpers import create_config_file, create_git_hooks


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


def test_git_hook_creation(workspace_with_git):
    """create_git_hooks helper function should create hooks files in the git hook folder"""
    githooks_dir = os.path.join(workspace_with_git, '.git/hooks')
    assert os.path.isfile(os.path.join(githooks_dir, 'pre-commit')) is False
    configfile_path = os.path.join(workspace_with_git, '.githooks.ini')
    create_config_file(configfile_path=configfile_path)
    create_git_hooks(configfile_path, githooks_dir)
    assert os.path.isfile(os.path.join(githooks_dir, 'pre-commit')) is True


def test_git_hook_creation_permissions(workspace_with_git):
    """create_git_hooks helper function should create hooks files with correct permissions"""
    githooks_dir = os.path.join(workspace_with_git, '.git/hooks')
    configfile_path = os.path.join(workspace_with_git, '.githooks.ini')
    create_config_file(configfile_path=configfile_path)
    create_git_hooks(configfile_path, githooks_dir)
    assert os.access(os.path.join(githooks_dir, 'pre-commit'), os.X_OK) is True


def test_git_hook_creation_exit(mocker, workspace_with_git):
    """create_git_hooks helper function should exit if not valid configuration file is provided"""
    mocked_sys_exit = mocker.patch('sys.exit')
    githooks_dir = os.path.join(workspace_with_git, '.git/hooks')
    create_git_hooks('wrong_config_file.ini', githooks_dir)
    mocked_sys_exit.assert_called_once_with(1)
