
__author__ = 'Waqas Younas'

"""
Homer: A text analyzer.
"""

# Always prefer setuptools over distutils
import os
from setuptools import setup
from distutils.command.install import install as _install
# To use a consistent encoding
from codecs import open

this_directory = os.path.abspath(os.path.dirname(__file__))


class install(_install):
    def run(self):
        _install.run(self)
        import nltk
        nltk.download('punkt')
        # after punkt is install, let's install other packages one by one
        nltk.download('averaged_perceptron_tagger')
        nltk.download('cmudict')
        nltk.download('stopwords')


with open(os.path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='homer_text',
    version='0.4.1',
    description='Homer, a text analyser in Python, can help make your text more clear, simple and useful for your readers.',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['homer'],
    packages_dir={'homer': 'homer'},
    include_package_data=True,
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # What does your project relate to?
    keywords='text analyzer',
    project_urls={
        "Bug Tracker": "https://github.com/wyounas/homer/issues",
        "Documentation": "https://github.com/wyounas/homer",
        "Source Code": "https://github.com/wyounas/homer",
    },

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
        'nltk==3.4.1',
        'Pyphen==0.9.5',
        'repoze.lru==0.7',
        'six==1.12.0',
        'terminaltables==3.1.0',
        'textstat==0.5.6',
    ],
    setup_requires=['nltk==3.4.1'],
    cmdclass={'install': install}
)


