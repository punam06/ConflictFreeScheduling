#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script for Conflict-Free Scheduling System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="conflict-free-scheduling",
    version="1.0.0",
    author="CSE Department",
    author_email="cse@bup.edu.bd",
    description="A comprehensive conflict-free scheduling system for academic institutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/conflict-free-scheduling-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
        ],
        "pdf": [
            "reportlab>=3.6.0",
            "weasyprint>=56.0",
        ],
        "web": [
            "flask>=2.2.0",
            "gunicorn>=20.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "conflict-scheduler=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.csv", "*.json"],
    },
    keywords="scheduling, optimization, algorithms, academic, university, conflict-free",
    project_urls={
        "Bug Reports": "https://github.com/your-username/conflict-free-scheduling-python/issues",
        "Source": "https://github.com/your-username/conflict-free-scheduling-python",
        "Documentation": "https://github.com/your-username/conflict-free-scheduling-python/wiki",
    },
)
