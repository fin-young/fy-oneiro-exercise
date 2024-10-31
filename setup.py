from setuptools import setup, find_packages

requirements = open("requirements.txt", "r").readlines()
version = open("version.txt", "r").read().strip()

setup(
    name="fy-oneiro-exercise",
    version=version,
    description="Calculating a simple loan via a cmd",
    author="Finlay Young" ,
    url="https://github.com/fin-young/fy-oneiro-exercise.git",
    #packages=find_packages(exclude=[]),
    classifiers=[
        "Development Status :: Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.13",
    ],
    install_requires=requirements,
    extras_require={"test": ["pytest"]},
    include_package_data=True,
)