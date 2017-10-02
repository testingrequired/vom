from setuptools import setup, find_packages

setup(
    name="vom",
    version="0.1.1",
    description="An opinionated framework for writing page objects for selenium tests/scripts",
    author="Kylee Tilley",
    author_email="kyleetilley@gmail.com",
    url="https://github.com/testingrequired/vom",
    keywords=["selenium", "page-object", "testing", "automation", "test", "tests"],
    license="MIT",
    packages=find_packages(exclude=['venv', 'test']),
    install_requires=['selenium'],
    python_requires="~=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: User Interfaces"
    ]
)
