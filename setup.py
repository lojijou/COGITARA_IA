from setuptools import setup, find_packages

setup(
    name="cogitara_ia",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==3.0.0",
        "Flask-Session==0.5.0", 
        "Werkzeug==3.0.1",
        "psutil==5.9.6",
        "python-dotenv==1.0.0",
        "gunicorn==21.2.0",
        "blinker==1.7.0",
        "Jinja2==3.1.2",
    ],
    author="Cogitara IA Team",
    author_email="dev@cogitara.com",
    description="Advanced AI-powered web application with comprehensive features",
    keywords="ai flask web-application analytics",
    python_requires=">=3.8",
)
