import setuptools


setuptools.setup(
    author="Conrad Bzura",
    author_email="conradbzura@gmail.com",
    entry_points={
        "versioning.plugins": [
            "git=src.versioning._git"
        ],
    },
    include_package_data=True,
    install_requires=["GitPython"],
    name="versioning",
    packages=setuptools.find_packages(include=["src"]),
    package_dir={"": "src"},
    version="0.1.0-rc1",
)
