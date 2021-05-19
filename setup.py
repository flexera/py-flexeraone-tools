from setuptools import setup
import os

test_deps = [
    'coverage',
    'pytest',
    'pylint',
    'flake8',
    'autopep8'
]

dev_deps = [
    'pydoc-markdown'
]

extras = {
    'test': test_deps,
    'dev': dev_deps
}
readme = open('README.md', 'r+')

setup(
    name="py-flexeraone-tools",
    version="0.0.1",
    author="Flexera",
    author_email="support@flexera.com",
    description=("A collection of tools to work with the FlexeraOne APIs"),
    license_files=('LICENSE'),
    keywords="",
    url="https://github.com/flexera/py-flexeraone-tools",
    packages=['py-flexeraone-tools', 'tests'],
    long_description=readme.read(),
    classifiers=[],
    # Other metadata...
    tests_require=test_deps,
    extras_require=extras,
)
