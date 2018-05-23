import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ShallowOceanExpedition",
    version="0.1.2",
    author="Theo Windebank",
    author_email="windebank.theo@gmail.com",
    description="Simulate runs of a game with the ability to define custom strategies.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twindebank/ShallowOceanExpedition",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)