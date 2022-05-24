from setuptools import setup, find_packages

def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()

def get_name():
    return 'satori'

def get_version():
    return '0.0.1'

setup(
    name=get_name(),
    version=get_version(),
    description='A framework and engine that builds and uses simple preditive models.',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=[f'{get_name()}.{p}' for p in find_packages(where=get_name())],
    install_requires=[],
    python_requires='>=9.5',
    author='Jordan Miller',
    author_email="paradoxlabs@protonmail.com",
    url=f"https://github.com/lastmeta/{get_name()}",
    download_url='https://github.com/lastmeta/Satori',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    #entry_points={
    #    "console_scripts": [
    #        f"spe = {get_name()}.cli.{get_name()}:main",
    #    ]
    #},
)
