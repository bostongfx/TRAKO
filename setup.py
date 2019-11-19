import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trako", # Replace with your own username
    version="0.2",
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
)
