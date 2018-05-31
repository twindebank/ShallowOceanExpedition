from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="ShallowOceanExpedition",
        version="0.1.4",
        author="Theo Windebank",
        author_email="windebank.theo@gmail.com",
        description="Simulate runs of a game with the ability to define custom strategies.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/twindebank/ShallowOceanExpedition",
        packages=find_packages(),
        classifiers=(
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        install_requires=[
            'cycler==0.10.0',
            'kiwisolver==1.0.1',
            'matplotlib==2.2.2',
            'numpy==1.14.3',
            'pyparsing==2.2.0',
            'python-dateutil==2.7.3',
            'pytz==2018.4',
            'six==1.11.0',
            'tqdm==4.23.4'
        ]
    )
