#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt', session=PipSession())]

test_requirements = [str(ir.req) for ir in parse_requirements('requirements_test.txt', session=PipSession())]

setup(
    name='data-refinery',
    version='0.1.0',
    description="",
    long_description=readme + '\n\n',
    author="Innovation-Labs",
    license="Apache 2.0, Copyright 2018 - Banco Bilbao Vizcaya Argentaria S.A.",
    url='ssh://git@github.com:BBVA/data-refinery.git',
    packages=find_packages(include=['data-refinery']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='data-refinery',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    test_suite='tests',
    tests_require=test_requirements
)
