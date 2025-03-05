from setuptools import setup, find_packages

setup(
    name="apiseek",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "apiseek": ["templates/*.html", "static/*.*"],
    },
    install_requires=[
        "fastapi",
        "jinja2",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A custom API dashboard for FastAPI endpoints.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/apiseek",  # Update this with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
