"""Package Setup for Django Replay
"""

import pathlib
import re

import setuptools
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        exit(errno)


init = (pathlib.Path('replay') / '__init__.py').read_text()
match = re.search(r"^__version__ = '(.+)'$", init, re.MULTILINE)
version = match.group(1)

with open('README.rst') as reader:
    readme = reader.read()

setuptools.setup(
    name='django-replay',
    version=version,
    description='Record and replay Django web requests.',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='https://grantjenks.com/docs/replay/',
    license='Apache 2.0',
    packages=['replay'],
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=['Django'],
    project_urls={
        'Documentation': 'https://grantjenks.com/docs/replay/',
        'Source': 'https://github.com/grantjenks/django-replay',
        'Tracker': 'https://github.com/grantjenks/django-replay/issues',
    },
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
