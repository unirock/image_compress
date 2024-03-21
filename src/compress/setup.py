from setuptools import setup

setup(
    name="foo",
    version="0.1",
    py_modules=["compress"],
    entry_points={"console_scripts": ["compress = compress:entry"]},
)
