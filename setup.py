from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import RunITC

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='RunITC',
    version=RunITC.__version__,
    url='http://github.com/konchris/RunITC/',
    license='GNU GPLv2',
    author='Christopher Espy',
    tests_require=['pytest'],
    install_requires=['py==1.4.26',
                      'pytest==2.7.0',
                      ],
    cmdclass={'test': PyTest},
    # entry_points={
    #     'gui_scripts': [
    #         'runitc = RunITC.runitc:main'
    #         ]
    #     },
    scripts=['RunITC/runitc.py'],
    author_email='github@konchris.de',
    description="Tool for running an Oxford Instruments ITC 503",
    long_description=long_description,
    packages=['RunITC'],
    include_package_data=True,
    platforms='any',
    test_suite='RunITC.test.test_runitc.py',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt'
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization'
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
