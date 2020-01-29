#!/usr/bin/env python

from setuptools import setup

setup(
    name="Flask-IPFS",
    # NOTE Version managed by bumpversion
    version="0.1.0-alpha.3",
    url="https://github.com/zatoichi-labs/Flask-IPFS",
    license="MIT",
    author="Zatoichi Labs",
    author_email="admin@zatoichilabs.com",
    description="IPFS Plugin for Flask",
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    py_modules=["flask_ipfs"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "Flask",
        "ipfshttpclient",
        "multiaddr",
    ],
    extras_require={
        "dev": [
            "bumpversion",
            "ipython",
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
