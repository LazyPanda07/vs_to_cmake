from setuptools import find_packages
from setuptools import setup

setup(
    name="vs_to_cmake",
    version="v0.1.0",
    packages=find_packages(),
    install_requires=[
        "tqdm",
        "xmltodict"
    ],
    description="Convert *.sln or *.vcxproj to CMakeLists.txt for C++ projects.",
    author="LazyPanda07",
    author_email="semengricenko@gmail.com",
    url="http://github.com/LazyPanda07/vs_to_cmake",
    license="MIT",
    keywords="Converter",
    entry_points={"console_scripts": ["vs_to_cmake=vs_to_cmake.cli:main"]},
)
