import os
import ast

from setuptools import setup, find_packages

# To use a consistent encoding
import codecs


# pitfalls of python package versioning:
# 1. https://packaging.python.org/guides/single-sourcing-package-version/
# 2. https://milkr.io/kfei/5-common-patterns-to-version-your-Python-package


def local_scheme(version):
    return ""


def version_scheme(version):
    return str(version.tag)


setup(
    name="hey",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    setup_requires=["setuptools_scm"],
    use_scm_version={"version_scheme": version_scheme, "local_scheme": local_scheme},
    description="hey hey",
    long_description="hey hey hey",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
    ],
    # What does your project relate to?
    keywords="hey",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["docs", "*tests*", "examples"]),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["PyGithub==1.43.2", "pyyaml==3.13", "black"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={"dev": ["twine", "wheel"], "test": ["flake8==3.5.0", "pylint==2.1.1"]},
)

# python packaging documentation:
# 1. https://python-packaging.readthedocs.io/en/latest/index.html
# 2. https://python-packaging-user-guide.readthedocs.io/tutorials/distributing-packages
# a) pip install wheel twine
# b) pip install -e .
# c) python setup.py sdist
# d) python setup.py bdist_wheel
# e) DONT use python setup.py register and python setup.py upload. They use http
# f) twine upload dist/* -r testpypi
# g) pip install -i https://testpypi.python.org/pypi <package name>
# h) twine upload dist/*   # prod pypi
# i) pip install <package name>
# pip install -e .[dev,test]
