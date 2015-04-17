from setuptools import setup
setup(
    name="osnames",
    version="0.1.1",
    description="A command to search and clone openstack projects",
    url="https://github.com/huanghao/openstack-project-names",
    scripts=["osnames"],
    install_requires=['requests', 'requests-cache'],
)
