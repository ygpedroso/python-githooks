import pathlib
from python_githooks.__main__ import main, get_config_file_path
import python_githooks


def test_main_entry_point_exit(mocker, workspace_without_git_path):
    """main function should exit if ran in not valid git project"""
    # workspace_without_git_path is already a pathlib.Path from conftest.py
    # We need to mock the module-level variables in __main__
    mocker.patch.object(python_githooks.__main__, '__BASE_DIR__', workspace_without_git_path)
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_BASE_DIR__', workspace_without_git_path / ".not_git" / "hooks")
    # Explicitly set the config file paths as well, as get_config_file_path will use them
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YAML_PATH__', workspace_without_git_path / ".githooks.yml")
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YML_PATH__', workspace_without_git_path / ".githooks.yaml")

    mocked_sys_exit = mocker.patch('sys.exit')
    main()
    mocked_sys_exit.assert_called_once_with(1)


def test_main_entry_point_config_file_creation(mocker, workspace_with_git_path):
    """main function should create .yml config file if it doesn't exists"""
    # workspace_with_git_path is already a pathlib.Path from conftest.py
    mocker.patch.object(python_githooks.__main__, '__BASE_DIR__', workspace_with_git_path)
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_BASE_DIR__', workspace_with_git_path / ".git" / "hooks")
    # Ensure get_config_file_path returns the .yml path for creation
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YAML_PATH__', workspace_with_git_path / ".githooks.yml")
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YML_PATH__', workspace_with_git_path / ".githooks.yaml")

    # Make sure no config file exists initially
    if (workspace_with_git_path / ".githooks.yml").exists():
        (workspace_with_git_path / ".githooks.yml").unlink()
    if (workspace_with_git_path / ".githooks.yaml").exists():
        (workspace_with_git_path / ".githooks.yaml").unlink()

    mock_create_config = mocker.spy(python_githooks.__main__, 'create_config_file')
    mock_create_hooks = mocker.spy(python_githooks.__main__, 'create_git_hooks')

    main()

    assert mock_create_config.call_count == 1
    # Check that create_config_file was called with the .yml path
    expected_config_path = workspace_with_git_path / ".githooks.yml"
    assert mock_create_config.call_args[1]['configfile_path'] == expected_config_path
    assert mock_create_hooks.call_count == 1
    assert (workspace_with_git_path / ".githooks.yml").is_file()


def test_get_config_file_path_prioritizes_yml(mocker, tmp_path):
    """get_config_file_path should prioritize .yml over .yaml if both exist."""
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YAML_PATH__', tmp_path / ".githooks.yml")
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YML_PATH__', tmp_path / ".githooks.yaml")

    (tmp_path / ".githooks.yml").touch()
    (tmp_path / ".githooks.yaml").touch()
    assert get_config_file_path() == tmp_path / ".githooks.yml"

def test_get_config_file_path_uses_yaml_if_yml_absent(mocker, tmp_path):
    """get_config_file_path should use .yaml if .yml is absent."""
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YAML_PATH__', tmp_path / ".githooks.yml")
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YML_PATH__', tmp_path / ".githooks.yaml")

    (tmp_path / ".githooks.yaml").touch()
    assert get_config_file_path() == tmp_path / ".githooks.yaml"

def test_get_config_file_path_defaults_to_yml_if_none_exist(mocker, tmp_path):
    """get_config_file_path should default to .yml for creation if neither exists."""
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YAML_PATH__', tmp_path / ".githooks.yml")
    mocker.patch.object(python_githooks.__main__, '__GITHOOKS_CONFIGFILE_YML_PATH__', tmp_path / ".githooks.yaml")

    assert get_config_file_path() == tmp_path / ".githooks.yml"
