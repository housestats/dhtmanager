from setuptools import setup, find_packages

setup(
    name='dhtmanager',
    version='0.1',
    author='Lars Kellogg-Stedman',
    author_email='lars@oddbit.com',
    description='web application for managing wireless sensors',
    license='GPLv3',
    url='https://github.com/larsks/dhtmanager',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pony',
        'psycopg2',
    ]
)
