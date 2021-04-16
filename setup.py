from os import path
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='assign-reviewers',
    version='0.2.3',
    author='Julien Cohen-Adad',
    author_email='jcohen@polymtl.ca',
    packages=find_packages(),
    url='https://github.com/jcohenadad/assign-reviewers',
    license='LICENSE',
    description='Assign reviewers and create scoring excel sheets.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # install_requires=requirements,
    entry_points={
        'console_scripts': [
            'assign-reviewers = assign_reviewers.assign_reviewers:main',
            ]
        },
    install_requires=[
        "pandas",
        "pytest",
        "pytest-cov",
        ]
    )
