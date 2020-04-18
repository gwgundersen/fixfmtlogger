#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for Flogger."""

from setuptools import setup


# -----------------------------------------------------------------------------

description = 'Flogger is a module for logging with fixed-width data.'

setup_args = dict(
    name='flogger',
    version='0.0.1',
    license='MIT',
    author='Gregory Gundersen',
    author_email='greg@gregorygundersen.com',
    description=description,
    url='https://github.com/gwgundersen/flogger',
    install_requires=['fixfmt'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)


def main():
    setup(**setup_args)


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
