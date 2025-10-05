from setuptools import setup, find_packages

setup(
    name="cogitara-ia",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.28.0",
        "pandas==2.0.3", 
        "numpy==1.24.3",
        "plotly==5.15.0",
        "textblob==0.17.1",
    ],
)