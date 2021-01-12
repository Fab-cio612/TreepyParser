import setuptools

with open("README.md", "r", encoding="utf-8") as rm:
    readme = rm.read()

setuptools.setup(
    name="TreepyParser",
    version="1.0.0",
    author="Fabio Cioni",
    author_email="fab.cioni6@gmail.com",
    description="A python library that parses html into a tree structure",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Fab-cio612/TreepyParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)