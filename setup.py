import os
from setuptools import setup


setup(
    name = "privoxy_pool",
    version = "1.1",
    author = "detonavomek",
    author_email = "detonavomek@gmail.com",
    description = ("Pool Privoxies controller"),
    license = "BSD",
    keywords = "privoxy controller",
    url = "http://github.com/Detonavomek/privoxy-pool",
    packages=['privoxy_pool'],
    long_description="Pool Privoxies controller",
    install_requires=[
        "tor-pool",
    ],
    dependency_links=[
        'http://github.com/Detonavomek/tor-pool#egg=tor-pool',
    ],
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
