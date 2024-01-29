import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

DEV_REQUIREMENTS = [
    'black',
    'coveralls == 3.*',
    'flake8',
    'isort',
    'pytest == 6.*',
    'pytest-cov == 2.*',
]

setuptools.setup(
    name='dir-diff-tool',
    version='1.0.0',
    description='Display a diff between two directories in HTML.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    author='DavidNaumann',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    entry_points={
        'console_scripts': [
            'dir_diff-tool=dir_diff_tool.cli:main',
        ],
    },
    python_requires='>=3.7, <4',
)