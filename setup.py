from setuptools import setup, find_packages


def desc():
    with open("README.md") as f:
        return f.read()

def reqs():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='frasco-api',
    version='0.1',
    url='http://github.com/frascoweb/frasco-api',
    license='MIT',
    author='Maxime Bouroumeau-Fuseau',
    author_email='maxime.bouroumeau@gmail.com',
    description="Create APIs and service based applications with Frasco",
    long_description=desc(),
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'frasco',
        'frasco-models',
        'frasco-users'
    ]
)