import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="python-githooks",
    version="1.0.2",
    description="Create git hooks with ease using a simple configuration file in a git project",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ygpedroso/python-githooks",
    author="Yannier González Pedroso",
    author_email="ygpedroso2503@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
    ],
    packages=["python_githooks"],
    include_package_data=True,
    install_requires=["configparser"],
    entry_points={
        "console_scripts": [
            "githooks=python_githooks.__main__:main",
        ]
    },
)
