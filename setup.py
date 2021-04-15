from setuptools import setup, find_packages

setup(
    name='assign-reviewers',
    version='0.1.4',
    author='Julien Cohen-Adad',
    author_email='jcohen@polymtl.ca',
    packages=find_packages(),
    url='https://github.com/jcohenadad/assign-reviewers',
    license='LICENSE',
    description='Assign reviewers and create scoring excel sheets.',
    long_description=open('README.md').read(),
    # install_requires=requirements,
    entry_points={
        'console_scripts': [
            'assign-reviewers = assign_reviewers:main',
            ]
        },
    install_requires=[
        "pandas",
        "pytest",
        "pytest-cov",
        ]
    )
