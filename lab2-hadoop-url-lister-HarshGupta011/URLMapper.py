#!/usr/bin/env python
"""url_mapper.py"""

import sys
import re
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    
    regex = 'href=(\"[^"]*\")'
    urls = re.findall(regex,line)
    for url in urls:
        print('%s\t%s' % (url, 1))
