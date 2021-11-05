#!/usr/bin/env python3
# vim:set ff=unix expandtab ts=4 sw=4:
from setuptools import setup, find_packages
def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="ComputabilityGraphs",
    version="0.9",
    #test_suite="example_package.tests",  # http://pythonhosted.org/setuptools/setuptools.html#test
    description="Deternmines computability of instances of a type based on a set of type annotated functions",
    long_description=readme(),  # avoid duplication
    author="Markus Müller",
    author_email="markus.mueller.1.g@gmail.com",
    #url="https://github.com/MPIBGC-TEE/ComputabilityGraphs",
    packages=find_packages('src'),  # find all packages (multifile modules) recursively
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        #"Operating System :: POSIX :: Linux",
        "Topic :: Education ",
    ],
    # entry_points={
    #'console_scripts': [
    #        'render= bgc_md.reports:render_parse'
    #        ]
    # },
    install_requires=[
        "frozendict",
        "testinfrastructure",  # also on https://github.com/MPIBGC-TEE/testinfrastructure.githttps://github.com/MPIBGC-TEE/testinfrastructure.git
        "networkx",
        "pygraphviz",
    ],
        include_package_data=True,
        zip_safe=False
)
