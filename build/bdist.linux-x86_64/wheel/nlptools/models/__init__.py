import os

modele_init_en = os.path.join(
    os.path.dirname(__file__), "en_core_web_sm-3.0.0", "en_core_web_sm-3.0.0"
)
modele_init_fr = os.path.join(
    os.path.dirname(__file__), "fr_core_news_sm-3.0.0/fr_core_news_sm", "fr_core_news_sm-3.0.0"
)
__all__ = [
    "modele_init_fr",
    "modele_init_en"
]
