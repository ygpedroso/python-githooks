hook_template = '''#!/usr/bin/env python

import os
import sys

def main():
    os.system("{command}")
    sys.exit(0)
    

if __name__ == "__main__":
    main()
'''
