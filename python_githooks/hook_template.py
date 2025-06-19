hook_template = '''#!/usr/bin/env python

import subprocess
import sys

def main():
    print("python-githooks > {section}")
    commands = {commands_list_str}  # This will be a list of strings

    for command in commands:
        print(f"Executing: {{command}}")
        try:
            # Using check_call to raise an exception on non-zero exit codes
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Command '{{command}}' failed with exit code {{e.returncode}}.")
            sys.exit(e.returncode)
        except Exception as e:
            print(f"An error occurred while executing '{{command}}': {{e}}")
            sys.exit(1)
    sys.exit(0) # All commands succeeded


if __name__ == "__main__":
    main()
'''
