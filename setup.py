
"""Diff measurement for Python"""

# Setuptools has to be imported before distutils, or things break.
from setuptools import setup

# PYVERSIONS
classifiers = """\
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Programming Language :: Python :: 3.12
Programming Language :: Python :: 3.13
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Topic :: Software Development :: Quality Assurance
Topic :: Software Development :: Testing
"""

# Create the keyword arguments for setup()

setup_args = dict(
    name="diff",
    version="1.0.0",
    packages=[
        "diff",
    ],
    package_data={
        "diff": [
            "templates/*.*"
        ]
    },
    entry_points={
        # Install a script as "coverage", and as "coverage3", and as
        # "coverage-3.7" (or whatever).
        "console_scripts": [
            "diff = diff.cli:main",
        ],
    },
    dependencies=[
        "Jinja2>=3.1.2"
    ],
    # We need to get HTML assets from our htmlfiles directory.
    zip_safe=False,
    author="David Naumann",
    author_email="dnaumann@bastiansolutions.com",
    description="",
    long_description="long_description",
    long_description_content_type="text/x-rst",
    keywords="diff comparison tool",
    license="Apache-2.0",
    license_files=["LICENSE.txt"],
    url="https://github.com/DavidNaumann/diff",
    project_urls={},
    python_requires=">=3.8",  # minimum of PYVERSIONS
)

def main():
    """Actually invoke setup() with the arguments we built above."""
    # For a variety of reasons, it might not be possible to install the C
    # extension.  Try it with, and if it fails, try it without.
    setup(**setup_args)


if __name__ == "__main__":
    main()