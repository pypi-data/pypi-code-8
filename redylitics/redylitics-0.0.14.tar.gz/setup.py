from distutils.core import setup


setup(
    name="redylitics",
    version="0.0.14",
    description="Read and Write Event Data to Redis",
    author="Vince Forgione",
    author_email="vforgione@theonion.com",
    packages=["redylitics"],
    install_requires=[
        "gevent==1.0.1",
        "redis==2.10.3",
    ],
    url="https://github.com/theonion/redylitics"
)
