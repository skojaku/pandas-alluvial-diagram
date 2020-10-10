from setuptools import setup, find_packages

__version__ = "0.0.1"

setup(
    name="cpnet",
    version=__version__,
    author="Sadamori Kojaku",
    author_email="freesailing4046@gmail.com",
    description="Drawing alluvial digram from pandas",
    long_description="Drawing alluvial digram from pandas",
    url="https://github.com/skojaku/pandas-alluvial-diagram",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["numpy>=1.16.0", "scipy>=1.5.2", "matplotlib>=3.1.3",],
    zip_safe=False,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="alluvial diagram, pandas",
)
