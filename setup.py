from setuptools import setup, find_packages

setup(
    name="nur-update",
    version="1.0.0",
    url="https://github.com/nix-community/nur-update.git",
    author="Jörg Thalheim",
    author_email="joerg@thalheim.io",
    description="Description of my package",
    packages=find_packages(),
    install_requires=["flask"],
    entry_points={"console_scripts": ["nur-update-server=nur_update:main"],},
)
