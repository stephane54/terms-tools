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
    include_package_data=True,
    package_data={"": ["*.jsonl", "*.tsv", "*.json", "*.txt", "*.ini", "nlptools"]},
    author_email="stephane.schneider@inist.fr",
    maintainer="stephane",
    maintainer_email="stephane.schneider@inist.fr",
    keywords="nlp scientific package Python for computationnal terminology",
    classifiers=["Topic :: natural langage processsing", "Topic :: Documentation"],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["terms_tools = nlptools.terms_toolsCLI:console_scripts_main" ]
    },
    install_requires = reqs,
    #dependency_links = [
    #    'git+http://vxgit.intra.inist.fr:60000/git/RichText/spacy_lefff.git@0.4.1#egg=spacy_lefff',
    #],
    description="Bibliotheque de composants python NLP",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    license="GPL V3",
    url="https://github.com/stephane54/terms-tools.git",
    platforms="ALL",
    python_requires=">=3.6",
)
