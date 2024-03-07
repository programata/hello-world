import re
import sys

from kedro.framework.cli import main

if __name__ == '__run__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())