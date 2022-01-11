import os

from setuptools import find_namespace_packages, setup


with open(os.path.join("opensafely/core", "VERSION")) as f:
    version = f.read().strip()

setup(
    name="pipeline",
    version=version,
    packages=find_namespace_packages(exclude=["tests"]),
    include_package_data=True,
    url="https://github.com/opensafely/opensafely-cli",
    description="library for parsing OpenSAFELY project.yaml files.",
    license="GPLv3",
    author="OpenSAFELY",
    author_email="tech@opensafely.org",
    python_requires=">=3.8",
    classifiers=["License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    install_requires=[
        "jsonschema==3.2.0",
        "ruamel.yaml==0.17.7",
    ]
)
