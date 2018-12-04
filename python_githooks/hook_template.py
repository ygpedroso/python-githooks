hook_template = '''#!/usr/bin/env python

import os
import sys

def main():
    print("python-githooks > {section}")
    os.system("{command}")
    sys.exit(0)


if __name__ == "__main__":
    main()
'''
