# This is only a stub setup.py so tox can run its tests.
# You should not (yet?) use this to install the package.

from setuptools import setup

setup(
    name="mcstats",
    version="0.0.1",
    packages=['mcstats'],
    install_requires=[
        'flask',
        'beaker',
        'requests',
    ],
)
