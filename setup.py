import os
import sys
import shutil
import pathlib
import setuptools
import subprocess
from setuptools import setup

README = f"{pathlib.Path(__file__).parent}/README.md"

with open(README) as r:
    README = r.read()

setup(
    name='pug4py',
    version='1.0.1',
    author='Adriano Romanazzo (multiversecoder)',
    description='Pug4Py is a tool that allows you to integrate Pug js as a templating engine into any Python framework.',
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=["mako"],
    packages=['pug4py'],
    package_dir={'pug4py': 'pug4py'},
    include_package_data=True,
    url='https://github.com/multiversecoder/pug4py',
    download_url='https://pypi.python.org/pypi/pug4py',
    author_email='pythonmultiverse@gmx.com',
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: JavaScript',
    ],
)
