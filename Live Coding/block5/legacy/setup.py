from setuptools import setup, find_packages

setup(
    name="seminar-demo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic==2.14.4",
        "requests>=2.25,<3",
        "packaging>=21.0",
    ],
    python_requires=">=3.10",
)
