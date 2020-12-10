from distutils.core import setup
import os.path
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wisconsin_covid19",
    packages=setuptools.find_packages(),
    version="0.0.1",
    license="MIT",
    description="The Unofficial TikTok API Wrapper in Python 3.",
    author="David Teather",
    author_email="contact.davidteather@gmail.com",
    url="https://github.com/davidteather/Wisconsin-Covid19-API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/davidteather/Wisconsin-Covid19-API/tarball/master",
    keywords=["wisconsin", "covid19", "covid-19"],
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)