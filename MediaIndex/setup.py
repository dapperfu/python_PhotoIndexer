import os
import sys

from setuptools import find_packages, setup

import versioneer

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))


# Get requirements
requirements = []
with open(os.path.join(LOCAL_DIR, "requirements.txt"), "r") as infile:
    for line in infile:
        line = line.strip()
        if line and not line[0] == "#":  # ignore comments
            requirements.append(line)

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    name="MediaIndexer",
    author="Jed Frey",
    description="IndexMediaStuffs with Python & Redis.",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mi = MediaIndexer.cli:cli',
        ],
    }
)
