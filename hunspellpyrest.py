#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from xtsv import pipeline_rest_api, singleton_store_factory


hunspell_spell = ('hunspellpy', 'HunspellPy', 'spell',
                  (), {'task': 'spell', 'source_fields': {'form'}, 'target_fields': ['spell']})
hunspell_stem = ('hunspellpy', 'HunspellPy', 'stem',
                 (), {'task': 'stem', 'source_fields': {'form'}, 'target_fields': ['anas']})
hunspell_analyze = ('hunspellpy', 'HunspellPy', 'analyze',
                    (), {'task': 'analyze', 'source_fields': {'form'}, 'target_fields': ['anas']})
hunspell_dstem = ('hunspellpy', 'HunspellPy', 'dstem',
                  (), {'task': 'dstem', 'source_fields': {'form'}, 'target_fields': ['spell', 'anas']})


tools = [(hunspell_spell, ('spell',)),
         (hunspell_stem, ('stem',)),
         (hunspell_analyze, ('analyze',)),
         (hunspell_dstem, ('dstem',)),
         ]
app = pipeline_rest_api('HunspellPy', tools, {},  conll_comments=False, singleton_store=singleton_store_factory(),
                        form_title='emMorph demo', form_type='radio',
                        doc_link='https://github.com/dlt-rilmta/hunspellpy')

if __name__ == '__main__':
    app.run(debug=False)
