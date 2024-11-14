
__all__ = [
    'DICT_EDUCALINGO',
    'DICT_SYNONYMCOM',
    'DICT_THESAURUS',
    'DICT_WORDNET',
    'MultiDictionary'
]

import json
 
import PyMultiDictionary._utils as ut
import re
import urllib.error
import urllib.parse

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from typing import Dict, Tuple, Optional, List, Union
from warnings import warn

# Dicts
_EDUCALINGO_LANGS = ('bn', 'de', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'jv', 'ko', 'mr', 'ms', 'pl', 'pt', 'ro', 'ru', 'ta', 'tr', 'uk', 'zh', 'vi')

DICT_EDUCALINGO = 'educalingo'
DICT_SYNONYMCOM = 'synonym'
DICT_THESAURUS = 'thesaurus'
DICT_WORDNET = 'wordnet'
def translate(self, lang: str, word: str, to: str = '', dictionary: str = DICT_EDUCALINGO) -> TranslationType:
    """
    Translate a word.

    :param lang: Lang tag (ISO 639)
    :param word: Word to translate
    :param to: Target language (Google API)
    :param dictionary: Dictionary to retrieve the translations if ``to`` is empty
    :return: List of (Lang tag, translated word)
    """
    assert isinstance(lang, str), 'lang code must be an string'
    assert isinstance(to, str), 'to lang code must be an string'
    words = []
    word = self._process(word)

    assert dictionary in DICT_EDUCALINGO, 'Unsupported dictionary'    

    if lang not in self._langs.keys() or not self._langs[lang][2]:
        raise InvalidLangCode(f'{lang} code is not supported for translation')

    if lang in _EDUCALINGO_LANGS:
        bs = self.__search_educalingo(lang, word=word.replace(' ', '-'))
        if bs is None:
            return words
        results = [i for i in bs.find_all('div', {'class': 'traduccion0'})]
        if len(results) == 0:
            return words
        for j in results:
            lang_tag = j.get('id')
            lang_name = j.find_all('h4', {'class', 'traductor'})
            if len(lang_name) != 1:
                continue
            lang_name = lang_name[0].find_all('strong', {})
            if len(lang_name) != 1:
                continue
            # lang_name = lang_name[0].text.strip().capitalize()

            # Find non-links
            lang_nonlink = j.find_all('span', {'class': 'negro'})
            if len(lang_nonlink) == 1:
                words.append((lang_tag, lang_nonlink[0].text.strip()))
                continue

            # Find links
            lang_link = j.find_all('strong', {})
            if len(lang_link) != 2:
                continue
            lang_link = lang_link[1].find_all('a', {})
            if len(lang_link) == 1:
                words.append((lang_tag, lang_link[0].text.strip()))

        # Sort translations
        words = sorted(words, key=lambda x: x[0])

    # else:
    #     raise InvalidDictionary(f'Dictionary {dictionary} cannot handle language {lang}')

    return words