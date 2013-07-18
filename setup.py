from setuptools import setup, find_packages



requires = [
    #'lockfile==0.8',
    'python-daemon',
    'ConfigParser',
    'requests',
    ]

setup(
    name = "LBConverter",
    version = "0.1.2",
    author = "Lightbase",
    author_email = "breno.brito@lightbase.com.br",
    url = "https://pypi.python.org/pypi/LBConverter",
    description = "Daemon Converter for the neo-lightbase service",
    license = "GPLv2",
    keywords = "Converter extractor lightbase daemon",
    install_requires=requires,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: No Input/Output (Daemon)",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: Portuguese (Brazilian)",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database :: Database Engines/Servers",

    ]
)
