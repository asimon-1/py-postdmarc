"""Configure Python Packaging."""
from setuptools import setup, find_packages


setup(
    name="py-postdmarc",
    version="0.0.1",
    author="Andrew Simon",
    author_email="asimon1@protonmail.com",
    description=("A Python CLI interface for the Postmark DMARC monitoring API"),
    license="MIT",
    keywords="dmarc postmark forensic report",
    url="https://github.com/scuriosity/py-postdmarc",
    packages=find_packages(),
    install_requires=["dateparser>=0.7,<1.0", "requests>=2.0.0,<3.0", "fire>=0.3"],
    entry_points={"console_scripts": ["postdmarc = postdmarc.postdmarc:main"]},
)
