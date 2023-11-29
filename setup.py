#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ ]

test_requirements = [ ]

setup(
    author="Saketh Raj Bhattiprolu",
    author_email='saketh.bhattiprolu@stonybrook.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A specialized Python package dedicated to astronomical computations, deltascatter streamlines the process of selecting a narrow range of deflectors and listing corresponding source redshifts. Leveraging the capabilities of established libraries like astropy and lenstronomy, this package also offers tools to compute variations in the Einstein radius across different celestial populations for fixed source redshifts. Designed with simplicity and efficiency in mind, deltascatter aims to enhance astrophysical research and analysis workflows.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='deltascatter',
    name='deltascatter',
    packages=find_packages(include=['deltascatter', 'deltascatter.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Newton-Lightspeed/deltascatter',
    version='0.1.0',
    zip_safe=False,
)
