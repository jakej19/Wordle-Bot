from setuptools import setup, find_packages

setup(
    name="wordle_bot",
    version="1.0.0",
    author="Jacob Joyce",
    author_email="jacobajoyce@outlook.com",
    description="A Python-based Wordle solver and performance tester",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jakej19/Wordle-Bot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "tqdm",
        "colorama",
        "matplotlib",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "wordle-solver=wordle_bot:main",
            "wordle-tester=test_bot:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)
