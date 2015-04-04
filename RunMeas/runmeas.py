#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" The main script.

"""

__author__ = "Christopher Espy"
__copyright__ = "Copyright (C) 2014, Christopher Espy"
__credits__ = ["Christopher Espy"]
__license__ = "GPLv2"
__version__ = "0.0.1"
__maintainer__ = "Christopher Espy"
__email__ = "christopher.espy@uni-konstanz.de"
__status__ = "Development"

import sys


def main(argv=None):
    """The main function

    """

    if argv is None:
        argv = sys.argv

    print("Hello World!")

    sys.exit()

if __name__ == "__main__":
    main()
