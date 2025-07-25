from setuptools import setup, find_packages
import os

with open("requirements.txt") as f:
    reqs = f.read().splitlines()
    print(reqs)

with open("tag.txt") as f:
    version = f.read()

setup(
    name="terms-tools",
    version=version,
    zip_safe=False,
    author="stephane schneider",
    include_package_data=False,
    package_data={"": ["*.jsonl", "*.tsv", "*.json", "*.txt", "*.ini"]}, # "nlptools"
    exclude={'nlptools.models.*'},
    author_email="stephane.schneider@inist.fr",
    maintainer="stephane",
    maintainer_email="stephane.schneider@inist.fr",
    keywords="nlp scientific package Python for computationnal terminology on Loterre data",
    classifiers=["Topic :: natural langage processsing", "Topic :: Documentation"],
    packages=find_packages(exclude=['nlptools.models.*']),
    entry_points={
        "console_scripts": ["terms_tools = nlptools.terms_toolsCLI:console_scripts_main", "loterre_tag = nlptools.term_taggerCLI:console_scripts_main" ]
    },
    install_requires = reqs,
    description="Bibliotheque de composants python de computationnal terminology sur des données de la base Loterre",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    license="GPL V3",
    url="https://github.com/stephane54/terms-tools.git",
    platforms="ALL",
    python_requires=">=3.8",
)
