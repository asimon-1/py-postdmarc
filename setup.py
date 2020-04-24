"""Configure Python Packaging."""
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="py-postdmarc",
    version="0.0.1a",
    author="Andrew Simon",
    author_email="asimon1@protonmail.com",
    description=("A Python CLI interface for the Postmark DMARC monitoring API"),
    long_description_content_type="text/markdown",
    long_description=read("readme.md"),
    license="MIT",
    keywords="dmarc postmark forensic report",
    url="https://github.com/scuriosity/py-postdmarc",
    packages=find_packages(),
    install_requires=["dateparser>=0.7,<1.0", "requests>=2.0.0,<3.0", "fire>=0.3"],
    entry_points={"console_scripts": ["postdmarc = postdmarc.postdmarc:main"]},
)
