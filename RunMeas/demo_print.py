#!/usr/bin/env python
# coding: utf-8

"""The ITC Module.


"""

import time


def main():

    for i in range(100):
        time.sleep(0.1)
        print('Downloading {}\r'.format(i), end="")

if __name__ == "__main__":
    main()
