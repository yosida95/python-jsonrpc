# -*- coding: utf-8 -*-

import os

from setuptools import (
    find_packages,
    setup,
)

here = os.path.dirname(__file__)


def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except FileNotFoundError:
        return ""


setup(
    name='jsonrpc',
    version='0.2.0',
    description='A JSON RPC client library.',
    long_description=_read("README.rst"),
    url='https://github.com/yosida95/python-jsonrpc',

    author='Kohei YOSHIDA',
    author_email='kohei@yosida95.com',
    license='BSD-3-Clause',

    packages=find_packages(),
    python_requires='>= 3.5',
    install_requires=[],
    tests_require=[],

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
