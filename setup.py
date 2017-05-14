"""A setuptools based setup module for sharedmock.
"""

# template kindly provided by:
# https://github.com/pypa/sampleproject/blob/master/setup.py

# Always prefer setuptools over distutils
from codecs import open
from os import path

from setuptools import setup, find_packages


# To use a consistent encoding
here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sharedmock',
    version='0.1.0',
    description='A multiprocessing-friendly Python mock object',
    long_description=long_description,
    url='https://github.com/elritsch/python-sharedmock',
    author='Elmar Ritsch',
    author_email='elmar.ritsch@gmail.com',
    license='Apache v2.0',

    # from: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='testing multiprocessing development',
    packages=find_packages(exclude=['examples', '*.test']),
    install_requires=[],
    extras_require={
        'test': ['coveralls==1.1',
                 'prospector==0.12.4',
                 'pylint==1.6.5',
                 'pytest==3.0.5',
                 'pytest-cov==2.4.0'],
    },
)
