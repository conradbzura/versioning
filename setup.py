import setuptools


setuptools.setup(
    author="Conrad Bzura",
    author_email="conradbzura@gmail.com",
    entry_points={
        "versioning.plugins": [
            "git=src.versioning._git"
        ],
    },
    extras_require={
        "tests": ["pytest", "pytest-mock", "debugpy", "pyyaml"]
    },
    include_package_data=True,
    install_requires=["GitPython"],
    name="versioning",
    package_dir={"": "src"},
    packages=setuptools.find_packages(include=["src"]),
    version="0.1.0-rc1",
)
