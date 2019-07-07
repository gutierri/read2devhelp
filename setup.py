#!/usr/bin/env python3

from pathlib import Path

from setuptools import setup


with Path.cwd().joinpath('README.rst').open(encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='read2devhelp',
    version='0.1.0',
    description='Converts online README into DeveHelp2 books',
    long_description=long_description,
    author='Gutierri Barboza',
    author_email='pack+me@gutierri.me',
    python_requires='>=3.6.0',
    url='https://github.com/gutierri/read2devhelp',
    py_modules=['read2devhelp'],
    entry_points={
        'console_scripts': ['read2devhelp=read2devhelp:main'],
    },
    include_package_data=True,
    license='GPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development'
    ]
)
