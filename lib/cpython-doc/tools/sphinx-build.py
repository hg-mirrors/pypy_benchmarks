# -*- coding: utf-8 -*-
"""
    edited from the original, which was
    :copyright: 2007-2010 by Georg Brandl.
    :license: Python license.
"""

import sys
import os

if __name__ == '__main__':

    # mangle imports for docutils, since it is python-version specific
    mydir = os.path.dirname(__file__)
    import pprint
    pprint.pprint(sys.path)
    sys.path.append(mydir)
    if sys.version_info[0] < 3:
        sys.path.append(os.path.join(mydir, 'docutils2'))
    else:
        sys.path.append(os.path.join(mydir, 'docutils3'))

    from sphinx import main
    import time
    t0 = time.time()
    r = main(sys.argv)
    print(time.time() - t0)
    sys.exit(r)
