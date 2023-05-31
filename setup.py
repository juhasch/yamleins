from setuptools import find_packages, setup

setup(
    name="yamleins",
    version="0.0.1",
    author="Juergen Hasch",
    author_email="juergen.hasch@elbonia.de",
    description="Yaml configuration data with validation",
    license="BSD",
    python_requires=">=3.10",
    packages=find_packages(),
    requires=['PhysicalQuantities', 'yaml', 'wrapt'],
    long_description_content_type='text/markdown',
    long_description=""" Nothing yet""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
