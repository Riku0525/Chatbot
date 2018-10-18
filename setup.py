from setuptools import find_packages, setup

setup(
    # Application name:
    name="ChatbotANS",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Andres Barron",
    author_email="abg.ansconta@gmail.compile",

    # Packages
    packages=find_packages(),

    # Include additional files into the package
    include_package_data=True,

    zip_safe=False,

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)