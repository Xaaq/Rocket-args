"""The setup script."""

from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    version="0.1.0",
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
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="rocket_args",
    packages=["rocket_args"],
    url="https://github.com/Xaaq/rocket_args",
    install_requires=requirements,
    # TODO: check what below args do
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    include_package_data=True,
    keywords="rocket_args",
    test_suite="tests",
    zip_safe=False,
)
