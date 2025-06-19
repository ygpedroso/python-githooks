import os
import sys
import stat
import yaml
from .hook_template import hook_template


def create_config_file(configfile_path):
    dummy_config = {
        'pre-commit': {
            'commands': [
                'echo Pre commit hook installed.',
                'echo Replace these lines with your own commands.'
            ]
        }
    }
    with open(configfile_path, 'w') as configfile:
        yaml.dump(dummy_config, configfile, default_flow_style=False, sort_keys=False)


def create_git_hooks(configfile_path, githooks_dir):
    if not os.path.isfile(configfile_path):
        message = f'''
        Unable to find the "{configfile_path.name}" configuration file.
        Please, create it and try again.
        '''
        print(message)
        sys.exit(1)

    config = None
    with open(configfile_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {configfile_path.name}")
            print(exc)
            sys.exit(1)

    if not config:
        print(f"Warning: Configuration file '{configfile_path.name}' is empty. No hooks will be created.")
        return

    for hook_name, hook_config in config.items():
        if not isinstance(hook_config, dict):
            print(f"Warning: Invalid format for hook '{hook_name}' in '{configfile_path.name}'. Expected a dictionary. Skipping.")
            continue

        if 'commands' not in hook_config:
            print(f"Warning: Missing 'commands' key for hook '{hook_name}' in '{configfile_path.name}'. Skipping.")
            continue

        commands_list = hook_config['commands']
        if not isinstance(commands_list, list) or not all(isinstance(cmd, str) for cmd in commands_list):
            print(f"Warning: 'commands' for hook '{hook_name}' in '{configfile_path.name}' must be a list of strings. Skipping.")
            continue

        if not commands_list: # Handle empty commands list - similar to empty command before
            commands_list_str = "[]" # Empty list for the template
            print(f"Info: Hook '{hook_name}' has an empty commands list. It will do nothing.")
        else:
            # Ensure commands are properly escaped for the string representation in the template
            commands_list_str = "[" + ", ".join(f'"{cmd.replace("\"", "\\\"")}"' for cmd in commands_list) + "]"


        githook_file_path = os.path.join(githooks_dir, hook_name)
        try:
            with open(githook_file_path, 'wb') as file:
                # Pass the string representation of the list to the template
                file.write(hook_template.format(section=hook_name, commands_list_str=commands_list_str).encode())
            st = os.stat(githook_file_path)
            os.chmod(githook_file_path, st.st_mode | stat.S_IEXEC)
            if commands_list:
                 print(f"{hook_name} hook successfully created for running {len(commands_list)} command(s).")
            else:
                print(f"{hook_name} hook successfully created (will do nothing as commands list is empty).")

        except IOError as e:
            print(f"Error writing hook file for {hook_name}: {e}")
            # Decide if to sys.exit(1) or just skip this hook
        except Exception as e:
            print(f"An unexpected error occurred while creating hook {hook_name}: {e}")
