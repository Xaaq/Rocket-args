"""The setup script."""

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Amadeusz Hercog",
    author_email="xaaq333@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Make your arg parsing even more declarative!",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords="rocket_args",
    name="rocket_args",
    packages=["rocket_args"],
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Xaaq/rocket_args",
    version="0.1.0",
    zip_safe=False,
)
