# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

here = os.path.dirname(__file__)
requires = []
tests_require = []


def _read(name):
    try:
        return open(os.path.join(here, name)).read()
    except:
        return ""
readme = _read("README.rst")

setup(
    name='jsonrpc',
    version='0.1.1',
    description='A JSON RPC client library.',
    long_description=readme,
    url='https://github.com/yosida95/python-jsonrpc',

    author='Kohei YOSHIDA',
    author_email='kohei@yosida95.com',
    license='BSD-3-Clause',

    packages=find_packages(),
    install_requires=requires,
    tests_require=tests_require,

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
