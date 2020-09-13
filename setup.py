"""This will install csv2json_gen package

In order to install : pip install -e .
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv2json_gen",
    version="0.0.1",
    author="Tania Dawra",
    author_email="taniadawra11@gmail.com",
    description="Demo package for Morrison groceries: parse CSV data and generate JSON tree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
