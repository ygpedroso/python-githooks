hook_template = '''#!/usr/bin/env python

import subprocess
import sys

def main():
    print("python-githooks > {section}")
    return_code = subprocess.call("{command}",  shell=True)
    sys.exit(return_code)


if __name__ == "__main__":
    main()
'''
