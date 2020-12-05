from setuptools import setup, find_packages

setup(
    name="slvstopy",
    version="0.0.4",
    url="https://github.com/kktse/slvstopy",
    author="Kelvin Tse",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">3.6",
    install_requires=["Cython>=0.29.15", "python-solvespace>=3.0.2"],
    license="MPL2",
)
