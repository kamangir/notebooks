from setuptools import setup

from notebooks import NAME, VERSION, DESCRIPTION

setup(
    name=NAME,
    author="arash@kamangir.net",
    version=VERSION,
    description=DESCRIPTION,
    packages=[NAME],
)
