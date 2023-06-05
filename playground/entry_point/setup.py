from setuptools import setup

setup(
    name="greeter",
    version="1.0",
    packages=["greeter"],
    entry_points={"console_scripts": ["greeter = greeter.run:main"]},
)
