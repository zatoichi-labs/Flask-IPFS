#!/usr/bin/env python

from setuptools import (
    find_packages,
    setup,
)

setup(
    name="Flask-IPFS",
    # NOTE Version managed by bumpversion
    version="0.1.0-beta.5",
    url="https://github.com/zatoichi-labs/Flask-IPFS",
    license="MIT",
    author="Zatoichi Labs",
    author_email="admin@zatoichilabs.com",
    description="IPFS Plugin for Flask",
    setup_requires=['setuptools-markdown', 'wheel'],
    long_description_markdown_filename='README.md',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "Flask",
        "ipfshttpclient",
        "multiaddr",
        "py-cid",
    ],
    extras_require={
        "dev": [
            "bumpversion",
            "ipython",
            "pytest",
            "twine",
        ],
    },
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
