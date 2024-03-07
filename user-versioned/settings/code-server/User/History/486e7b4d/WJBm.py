import re
import sys

from kedro.framework.cli import main

import sys
#sys.path.append('/home/dataiku/workspace/project-lib-versioned/python/test_project/src')
#sys.path.append('/home/dataiku/workspace/project-lib-versioned/python/test_project')

def bk_main():
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())

if __name__ == '__main__':
    bk_main()
