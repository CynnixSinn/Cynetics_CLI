from setuptools import setup, find_packages

setup(
    name="cynetics-cli",
    version="0.1.0",
    description="The next-generation AI-driven command-line tool.",
    author="Cynetics Team",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "pyyaml>=6.0",
        "requests>=2.28",
        "rich>=13.0"
    ],
    entry_points={
        'console_scripts': [
            'cynetics=cynetics.cli.main:main',
        ],
    },
)