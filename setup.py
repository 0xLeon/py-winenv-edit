from setuptools import find_packages
from setuptools import setup

setup(
    name='winenv-edit',
    version='0.0.0',

    url='https://github.com/0xLeon/py-winenv-edit',
    author='Stefan Hahn',
    author_email='developement@0xleon.com',

    license='MIT',

    packages=find_packages(),

    install_requires=[
        'winenv',
        'elevate'
    ]
)
