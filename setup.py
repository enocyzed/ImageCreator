from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='ImageCreator',
    version='0.0.2',
    description='A software to create images from a yaml template',
    packages=['ImageCreator', 'ImageCreator.core'],
    package_dir={'': '.'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"

    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = [
        "pyyaml >= 5.1"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
    url="https://github.com/enocyzed/ImageCreator",
    author="Enoch",
    author_email="enocyzed@gmail.com",
    license="Apache License 2.0",

)