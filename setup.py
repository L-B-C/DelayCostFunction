from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = "Primary tactical gate-to-gate flight delay cost software simulator"
LONG_DESCRIPTION = ""

setup(
    name="DelayCostFunction",
    version=VERSION,
    author="LBC",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='git@github.com/L-B-C/DelayCostFunction.git',
    packages=find_packages(),
    license='MIT',
    install_requires=['pandas', 'numpy'],
    keywords=['flights', 'costs', 'cost model', 'delay', 'tactical','gate-to-gate'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    include_package_data=True
)