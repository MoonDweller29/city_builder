from setuptools import setup, find_packages
import glob
import os

def get_package():
    return glob.glob("city_builder/Resources/**/*", recursive=True)

def del_prefix(path):
    return os.path.relpath(path, "city_builder")

packages = list(map(del_prefix, glob.glob("city_builder/Resources/**/*", recursive=True)))
packages.append('Resources.json')

setup(
    name = 'city_builder',
    version = '1.0',
    packages=["city_builder", "city_builder.Sources"],
    install_requires=[
        'pygame>=2.0.1',
        'numpy>=1.13.3',
        'scikit-image>=0.13.1'
    ],
    entry_points={
        'console_scripts': [
            'city_builder=city_builder.__main__:main',
        ],
    },
    package_data={
        '': packages,
    },
)