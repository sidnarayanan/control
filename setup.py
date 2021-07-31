from setuptools import setup

reqs = open("requirements.txt", "r").readlines()
reqs = [l.strip() for l in reqs]

setup(
    name="control",
    version="0.0.1",
    packages=["control"],
    install_requires=reqs,
)
