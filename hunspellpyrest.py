#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from xtsv import pipeline_rest_api, singleton_store_factory
from hunspellpy import HunspellPy

hunspell_spell = (HunspellPy, (), {'task': 'spell', 'source_fields': {'form'}, 'target_fields': ['spell']})
hunspell_stem = (HunspellPy, (), {'task': 'stem', 'source_fields': {'form'}, 'target_fields': ['anas']})
hunspell_analyze = (HunspellPy, (), {'task': 'analyze', 'source_fields': {'form'}, 'target_fields': ['anas']})
hunspell_dstem = (HunspellPy, (), {'task': 'dstem', 'source_fields': {'form'}, 'target_fields': ['spell', 'anas']})

tools = {'spell': hunspell_spell, 'stem': hunspell_stem, 'analyze': hunspell_analyze, 'dstem': hunspell_dstem}

app = pipeline_rest_api('emMorph', tools, {},  conll_comments=False, singleton_store=singleton_store_factory())

if __name__ == '__main__':
    app.run(debug=False)
