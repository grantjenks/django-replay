from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import replay


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        exit(errno)


with open('README.rst') as reader:
    readme = reader.read()

setup(
    name='django-replay',
    version=replay.__version__,
    description='Record and replay web requests.',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='http://www.grantjenks.com/docs/replay/',
    license='Apache 2.0',
    packages=find_packages(exclude=('docs', 'tests')),
    tests_require=['tox'],
    cmdclass={'test': Tox},
    install_requires=[],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
