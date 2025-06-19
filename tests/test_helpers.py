import os
import yaml
import pathlib
from python_githooks.helpers import create_config_file, create_git_hooks


def test_config_file_creation_yaml(workspace_without_git_path):
    """create_config_file helper function should create .yml file"""
    configfile_path = pathlib.Path(workspace_without_git_path) / '.githooks.yml'
    create_config_file(configfile_path=configfile_path)
    assert configfile_path.is_file()


def test_config_file_default_values_yaml(workspace_without_git_path):
    """create_config_file helper function should create .yml file with default values and 'commands' list."""
    configfile_path = pathlib.Path(workspace_without_git_path) / '.githooks.yml'
    create_config_file(configfile_path=configfile_path)
    with open(configfile_path, 'r') as f:
        config = yaml.safe_load(f)
    assert list(config.keys()) == ['pre-commit']
    assert 'commands' in config['pre-commit']
    assert isinstance(config['pre-commit']['commands'], list)
    assert config['pre-commit']['commands'] == [
        'echo Pre commit hook installed.',
        'echo Replace these lines with your own commands.'
    ]


def test_git_hook_creation_yaml_with_commands_list(workspace_with_git_path):
    """create_git_hooks should create hook files from .yml with a 'commands' list."""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    config_data = {
        'pre-commit': {
            'commands': ['echo "Hello"', 'echo "World"']
        }
    }
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    with open(configfile_path, 'w') as f:
        yaml.dump(config_data, f)

    create_git_hooks(configfile_path, githooks_dir)
    assert pre_commit_hook_path.is_file()

    # Verify the content of the generated hook script
    hook_content = pre_commit_hook_path.read_text()
    assert 'commands = ["echo \\"Hello\\"", "echo \\"World\\""]' in hook_content
    assert 'for command in commands:' in hook_content
    assert 'subprocess.check_call(command, shell=True)' in hook_content


def test_git_hook_creation_permissions_yaml(workspace_with_git_path):
    """create_git_hooks helper function should create hooks files with correct permissions from .yml"""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    # Use default config file creation which now uses 'commands'
    create_config_file(configfile_path=configfile_path)
    create_git_hooks(configfile_path, githooks_dir)
    assert os.access(pre_commit_hook_path, os.X_OK)


def test_git_hook_creation_exit_on_invalid_yaml_file(mocker, workspace_with_git_path):
    """create_git_hooks should exit if the YAML configuration file is malformed."""
    mocked_sys_exit = mocker.patch('sys.exit')
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    invalid_config_path = pathlib.Path(workspace_with_git_path) / 'wrong_config_file.yml'
    with open(invalid_config_path, 'w') as f:
        f.write("pre-commit: [invalid_yaml") # Malformed YAML

    create_git_hooks(invalid_config_path, githooks_dir)
    mocked_sys_exit.assert_called_once_with(1)


def test_git_hook_creation_empty_config_yaml(capsys, workspace_with_git_path):
    """create_git_hooks should print a warning for empty YAML config and not create hooks"""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    with open(configfile_path, 'w') as f:
        yaml.dump({}, f) # Empty YAML (None after load)
    create_git_hooks(configfile_path, githooks_dir)
    captured = capsys.readouterr()
    assert f"Warning: Configuration file '{configfile_path.name}' is empty. No hooks will be created." in captured.out
    assert not pre_commit_hook_path.is_file()


def test_git_hook_creation_missing_commands_key(capsys, workspace_with_git_path):
    """create_git_hooks should warn and skip a hook if 'commands' key is missing."""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    config_data = {'pre-commit': {'command_typo': ['echo "test"']}} # Missing 'commands'
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    with open(configfile_path, 'w') as f:
        yaml.dump(config_data, f)

    create_git_hooks(configfile_path, githooks_dir)
    captured = capsys.readouterr()
    assert f"Warning: Missing 'commands' key for hook 'pre-commit' in '{configfile_path.name}'. Skipping." in captured.out
    assert not pre_commit_hook_path.is_file()

def test_git_hook_creation_commands_not_a_list(capsys, workspace_with_git_path):
    """create_git_hooks should warn and skip a hook if 'commands' is not a list."""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    config_data = {'pre-commit': {'commands': 'echo "not a list"'}}
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    with open(configfile_path, 'w') as f:
        yaml.dump(config_data, f)

    create_git_hooks(configfile_path, githooks_dir)
    captured = capsys.readouterr()
    assert f"Warning: 'commands' for hook 'pre-commit' in '{configfile_path.name}' must be a list of strings. Skipping." in captured.out
    assert not pre_commit_hook_path.is_file()

def test_git_hook_creation_commands_list_not_all_strings(capsys, workspace_with_git_path):
    """create_git_hooks should warn and skip a hook if 'commands' list contains non-strings."""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    config_data = {'pre-commit': {'commands': ['echo "valid"', 123]}} # Contains a number
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    with open(configfile_path, 'w') as f:
        yaml.dump(config_data, f)

    create_git_hooks(configfile_path, githooks_dir)
    captured = capsys.readouterr()
    assert f"Warning: 'commands' for hook 'pre-commit' in '{configfile_path.name}' must be a list of strings. Skipping." in captured.out
    assert not pre_commit_hook_path.is_file()


def test_git_hook_creation_with_empty_commands_list(capsys, workspace_with_git_path):
    """create_git_hooks should create a hook that does nothing if 'commands' list is empty."""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    config_data = {'pre-commit': {'commands': []}} # Empty commands list
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    with open(configfile_path, 'w') as f:
        yaml.dump(config_data, f)

    create_git_hooks(configfile_path, githooks_dir)
    captured = capsys.readouterr()
    assert f"Info: Hook 'pre-commit' has an empty commands list. It will do nothing." in captured.out
    assert pre_commit_hook_path.is_file()
    hook_content = pre_commit_hook_path.read_text()
    assert "commands = []" in hook_content # Ensure the template receives an empty list
    assert "for command in commands:" in hook_content # Loop should still be there

def test_git_hook_creation_invalid_top_level_format(capsys, workspace_with_git_path):
    """create_git_hooks should warn and skip if a top-level hook definition is not a dictionary."""
    githooks_dir = pathlib.Path(workspace_with_git_path) / '.git' / 'hooks'
    pre_commit_hook_path = githooks_dir / 'pre-commit'
    post_commit_hook_path = githooks_dir / 'post-commit'
    configfile_path = pathlib.Path(workspace_with_git_path) / '.githooks.yml'
    invalid_config = {
        'pre-commit': 'just a string, not a dict', # Invalid format
        'post-commit': {'commands': ['echo valid']}
    }
    with open(configfile_path, 'w') as f:
        yaml.dump(invalid_config, f)
    create_git_hooks(configfile_path, githooks_dir)
    captured = capsys.readouterr()
    assert f"Warning: Invalid format for hook 'pre-commit' in '{configfile_path.name}'. Expected a dictionary. Skipping." in captured.out
    assert not pre_commit_hook_path.is_file() # pre-commit should be skipped
    assert post_commit_hook_path.is_file() # post-commit should be created
    assert 'post-commit hook successfully created for running 1 command(s).' in captured.out
