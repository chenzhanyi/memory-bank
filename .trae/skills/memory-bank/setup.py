#!/usr/bin/env python3
"""
Memory Bank Setup
"""

from setuptools import setup, find_packages

setup(
    name="memory-bank",
    version="1.0.0",
    description="图书馆式记忆库 - 基于文件系统的智能体记忆管理系统",
    author="AI Assistant",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "memory-bank = memory_bank.cli:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
