import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="experimentcollector", # Replace with your own username
    version="0.1.0",
    author="Pakkapon Phongthawee",
    author_email="pakkapon.p_s19@vistec.ac.th",
    description="This is python library that use to store experiment result into sqlite then plot the result into scatter chart with trend line for analyze the trend of parameter.e",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pureexe/experiment-collector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={'experimentcollector': ['schema.sql']},
)