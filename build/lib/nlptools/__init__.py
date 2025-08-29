#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
# exemple :
import logging
__version__ = "0.4.0"
from configparser import ConfigParser
from .models import modele_init_en
from .models import modele_init_fr
from .tools import *
from .termMatcher import TermMatcher
from .POStagger import ViewPOStagger
from .POStagger import ViewPOStagger
from .lemma_lower import LowerCaseLemmas
from .NPchunker import NPchunker
from .NPchunkerDP import NPchunkerDP
#from .lefff import getLefff

__all__ = [
            "termMatcher",
            "NPchunker",
            "POStagger",
            "NPchunkerDP",
            "lefff",
            "matcherFlash"
            "LowerCaseLemmas"
            "matcherFlash",
]

logger = logging.getLogger(__name__)
logging.basicConfig()
