from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf8") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="redstorage",
    version="0.1.0",
    description="Library for writing sploits",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/b1n4r9/RedStorageLib",
    packages=find_packages(),
    install_requires=requirements,
)
