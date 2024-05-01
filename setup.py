from setuptools import setup

setup(
    name="cq_logging",
    version="0.1.0",
    description="Micropython logging, part of pimoroni:phew",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "GitHub": "https://github.com/c-and-q/cq-logging"
    },
    author="Jacek Banaszczyk",
    maintainer="Jacek Banaszczyk",
    maintainer_email="jacek.banaszczyk@gmail.com",
    license="MIT",
    license_files="LICENSE",
    packages=["cq/logging"]
)
