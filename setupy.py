from setuptools import setup, find_packages
from os import path

setup(

    name='pysniptips',

    version="0.1",

    description="Post Python Tips & Tricks with syntax highlighting to Twitter.",

    url="https://github.com/DmitrievichLevin/pysniptips",

    author='Jalin Howard',
    author_email='jhowar39@emich.edu',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],

    keywords='pygments syntax highlighting python pillow twitter tips tricks',

    packages=find_packages(),

    install_requires=['pillow', 'pygments', 'twitter', 'textwrap'],


)
