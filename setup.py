import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trako", 
    version="0.3.5.dev9",
    author="Daniel Haehn",
    author_email="haehn@mpsych.org",
    description="The TRAKO Project: Compression of DTI Streamlines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haehn/TRAKO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['scikit-build>=0.10.0'],
    scripts=['trakofy','untrakofy','tkompare'],
    install_requires=[
        'cycler>=0.10.0',
        'dataclasses>=0.6',
        'dataclasses-json>=0.3.6',
        'kiwisolver>=1.1.0',
        'marshmallow>=3.2.2',
        'marshmallow-enum>=1.5.1',
        'matplotlib>=3.1.1',
        'mypy-extensions>=0.4.3',
        'numpy>=1.17.4',
        'packaging>=19.2',
        'prettytable>=0.7.2',
        'pygltflib>=1.11.10',
        'pyparsing>=2.4.5',
        'python-dateutil>=2.8.1',
        'six>=1.13.0',
        'stringcase>=1.2.0',
        'TrakoDracoPy',
        'typing-extensions>=3.7.4.1',
        'typing-inspect>=0.5.0',
        'vtk>=8.1.2'
    ]
)
