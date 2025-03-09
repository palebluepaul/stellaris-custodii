from setuptools import setup, find_packages

setup(
    name="stellaris_custodii_tools",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "chardet",
    ],
    entry_points={
        'console_scripts': [
            'custodii-tools=stellaris_custodii_tools.custodii_tools:main',
        ],
    },
    author="Custodii Mod Team",
    author_email="example@example.com",
    description="Tools for developing the Custodii Race mod for Stellaris",
    keywords="stellaris, mod, tools",
    python_requires=">=3.6",
) 