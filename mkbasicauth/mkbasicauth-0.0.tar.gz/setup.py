from setuptools import setup


setup(
    name="mkbasicauth",
    version="0.0",
    description="Command to generate credential for Basic authentication",
    packages=["mkbasicauth"],
    entry_points={
        'console_scripts': [
            "mkbasicauth=mkbasicauth:main",
        ]
    }
)
