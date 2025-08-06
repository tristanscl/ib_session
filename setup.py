from setuptools import setup, find_packages

setup(
    name="ib_utils",
    version="0.1.0",
    description="Context manager for Interactive Brokers sessions with ib_async",
    author="Tristan Scuiller",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["ib_async"],
    python_requires=">=3.9",
)
