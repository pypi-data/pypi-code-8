from setuptools import setup

setup(
    name="pymold",
    version="0.1.0.1",
    description="A simple, fast template engine for Python.",
    long_description=open("README.md").read(),
    packages=[
        "mold",
    ],

    install_requires=[
    ],

    author="Bogdan Popa",
    author_email="popa.bogdanp@gmail.com",
    url="https://github.com/Bogdanp/mold",
    keywords=["web"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ]
)
