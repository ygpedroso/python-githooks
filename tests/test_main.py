import os
from python_githooks.__main__ import main
import python_githooks


def test_main_entry_point_exit(mocker, workspace_without_git):
    """main function should exit if ran in not valid git project"""
    python_githooks.__main__.__BASE_DIR__ = workspace_without_git
    python_githooks.__main__.__GITHOOKS_BASE_DIR__ = os.path.join(workspace_without_git, '.git/hooks')
    mocked_sys_exit = mocker.patch('sys.exit')
    main()
    mocked_sys_exit.assert_called_once_with(1)


def test_main_entry_point_config_file_creation(mocker, workspace_with_git):
    """main function should create config file if it doesn't exists"""
    python_githooks.__main__.__BASE_DIR__ = workspace_with_git
    python_githooks.__main__.__GITHOOKS_BASE_DIR__ = os.path.join(workspace_with_git, '.git/hooks')
    python_githooks.__main__.__GITHOOKS_CONFIGFILE_PATH__ = os.path.join(workspace_with_git, '.githooks.ini')
    mocker.spy(python_githooks.__main__, 'create_config_file')
    mocker.spy(python_githooks.__main__, 'create_git_hooks')
    main()
    assert python_githooks.__main__.create_config_file.call_count == 1
    assert python_githooks.__main__.create_git_hooks.call_count == 1
