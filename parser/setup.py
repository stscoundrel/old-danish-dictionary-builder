import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="old-danish-dictionary-builder-parser",
    version="1.0.0",
    author="stscoundrel",
    description="Parse OCR text pages to machine readable formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stscoundrel/old-danish-dictionary-builder",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
