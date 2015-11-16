#!/usr/bin/env python


from glob import glob


from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, "r") as f:
        for line in f:
            if line and line[:2] not in ("#", "-e"):
                yield line.strip()


setup(
    name="aws-utils",
    description="AWS Utilities",
    author="APN Online",
    author_email="dev.admin@apnonline.com.au",
    url="https://github.com/apnarm/aws-utils",
    license="MIT",
    packages=find_packages("."),
    scripts=glob("bin/*"),
    install_requires=list(parse_requirements("requirements.txt")),
    zip_safe=True,
)
