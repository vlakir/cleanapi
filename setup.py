from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['tornado>=6.1',
                'pydantic>=1.8.2',
                'asgiref>=3.3.4',
                'docutils>=0.17.1',
                'cryptography>=3.4.7',
                'keyring>=23.1.0',
                'requests>=2.26.0',
                'colorama>=0.4.4',
                'rfc3986>=1.5.0',
                'pkginfo>=1.7.1',
                'tqdm>=4.62.2',
                'urllib3>=1.26.6',
                'six>=1.16.0',
                'webencodings>=0.5.1',
                'packaging>=21.0',
                'bleach>=4.0.0',
                'certifi>=2021.5.30',
                'jeepney>=0.7.1',
                'SecretStorage>=3.3.1',
                'idna>=3.2',
                'Pygments>=2.10.0',
                'pyparsing>=2.4.7',
                'pycparser>=2.20',
                'zipp>=3.5.0'
                ]

setup(
    name="cleanapi",
    version="0.1.6",
    author="Vladimir Kirievskiy",
    author_email="vlakir1234@gmail.com",
    description="Pretty tornado wrapper for making lightweight REST API services",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/vlakir/cleanapi.git",
    # packages=['cleanapi', 'cleanapi.logger', 'cleanapi.third_party_libs'],
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers"
    ],
)
