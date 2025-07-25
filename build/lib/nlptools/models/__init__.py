import os
'''
# Version installation locale
modele_init_en = os.path.join(
    os.path.dirname(__file__), "en_core_web_trf-3.8.0-py3-none-any/en_core_web_trf", "en_core_web_trf-3.8.0"
)
modele_init_fr = os.path.join(
    os.path.dirname(__file__), "fr_dep_news_trf-3.8.0-py3-none-any/fr_dep_news_trf", "fr_dep_news_trf-3.8.0"
)
'''
__all__ = [
    "modele_init_fr",
    "modele_init_en"
]

# Version installation download
#MODEL_DIR="/home/schneist/app/terms_tools/terms_tools/nlptools/models"
print(os.environ.get('MODEL_DIR'))
 
modele_init_en = os.path.join(os.environ.get('MODEL_DIR'),"en_core_web_trf-3.8.0-py3-none-any/en_core_web_trf","en_core_web_trf-3.8.0")
modele_init_fr = os.path.join(os.environ.get('MODEL_DIR'),"fr_dep_news_trf-3.8.0-py3-none-any/fr_dep_news_trf","fr_dep_news_trf-3.8.0")


