
__author__ = 'Waqas Younas'

"""
Homer: A text analyzer.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.MD'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='homer',
    version='0.9,9',
    description='Homer: A text analyzer',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/wyounas/homer',

    # Author details
    author='Waqas Younas',
    author_email='waqas.younas@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4.5',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='Text Analyzer.',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'Click==7.0',
        'colorclass==2.2.0',
        'mongoengine==0.17.0',
        'nltk==3.4.1',
        'Pyphen==0.9.5',
        'repoze.lru==0.7',
        'six==1.12.0',
        'terminaltables==3.1.0',
        'textstat==0.5.6',
    ],
)
