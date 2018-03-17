from setuptools import setup

setup(
    name="automator",
    version="0.1.0",
    packages=['automator'],
    include_package_data=True,
    install_requires=[
        'psycopg2-binary'
    ],
)
