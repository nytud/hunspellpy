#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import hunspell
from json import dumps as json_dumps


class HunspellPy:
    def __init__(self, dic_file='/usr/share/hunspell/hu_HU.dic', aff_file='/usr/share/hunspell/hu_HU.aff',
                 task='dstem', source_fields=None, target_fields=None):
        """
        The initialisation of the module. One can extend the lsit of parameters as needed. The mandatory fields which
         should be set by keywords are the following:
        :param task: the task to specialise the current instance
        :param source_fields: the set of names of the input fields
        :param target_fields: the list of names of the output fields in generation order
        """
        # TODO: Heroku workaround for issue https://github.com/heroku/heroku-buildpack-apt/issues/35
        import os.path
        if not os.path.exists(dic_file):
            dic_file = '/app/.apt/usr/share/hunspell/hu_HU.dic'
            aff_file = '/app/.apt/usr/share/hunspell/hu_HU.aff'

        # Specialise the class for eg. stemming or detailed output...
        available_tasks = {'spell': self._do_spell, 'stem': self._do_stem, 'analyze': self._do_analyze,
                           'dstem': self._do_dstem}
        for keyword, key_fun in available_tasks.items():
            if task == keyword:
                self.process_token = key_fun
                break
        else:
            raise ValueError('No proper task is specified. The available tasks are {0}'.
                             format(' or '.join(available_tasks.keys())))

        # Field names for xtsv (the code below is mandatory for an xtsv module)
        if source_fields is None:
            source_fields = set()

        if target_fields is None:
            target_fields = []

        self.source_fields = source_fields
        self.target_fields = target_fields

        self.h = hunspell.HunSpell(dic_file, aff_file)
        self._added_words = set()
        self._removed_words = set()
        self._added_words_w_affix = {}

    @staticmethod
    def _split_anal(anal):
        anal_out = [tuple(a.split(':')) for a in anal.split(' ') if len(a) > 0]
        return anal_out

    def process_sentence(self, sen, field_names):
        for tok in sen:
            output = self.process_token(tok[field_names[0]])
            # Hunspell specific stuff, as spell goes in different field!
            if self.process_token in {self._do_dstem, self._do_spell}:
                tok.append(output.pop('spell', 'false'))
            if self.process_token != self._do_spell:  # TODO: Better way?
                output_json = json_dumps(output, ensure_ascii=False)
                tok.append(output_json)
        return sen

    @staticmethod
    def prepare_fields(field_names):
        return [field_names['form']]  # TODO: Maybe its not a good idea to hard-wire here the name of the features

    def _do_spell(self, tok):
        return {'spell': json_dumps(self.spell(tok), ensure_ascii=False)}  # Must retrieve string value in the dict!

    def _do_stem(self, tok):
        return {'stem': self.stem(tok)}

    def _do_analyze(self, tok):
        return {'anas': [self._split_anal(anal) for anal in self.analyze(tok)]}

    def _do_dstem(self, tok):
        return {'spell': json_dumps(self.spell(tok), ensure_ascii=False),  # Must retrieve string value in the dict!
                'stem': self.stem(tok), 'anas': [self._split_anal(anal) for anal in self.analyze(tok)]}

    def dstem(self, tok):
        return self._do_dstem(tok)

    def _decode_list(self, inp_list):
        enc = self.get_dic_encoding()
        return [e.decode(enc) for e in inp_list]

    def get_dic_encoding(self):
        """ Gets encoding of loaded dictionary. """
        return self.h.get_dic_encoding()

    def add_dic(self, dic_file):
        """ Adds extra dictionary """
        self.h.add_dic(dic_file)

    def add(self, word, example=None):
        """ Adds the given word with affix flags of the example (a dictionary word, when supplied)
             into the runtime dictionary """

        self._removed_words.discard(word)
        if example is not None:
            self._added_words_w_affix[word] = example  # Overwrite if exists...
            self.h.add_with_affix(word, example)
        else:
            self._added_words.add(word)
            self.h.add(word)

    def remove(self, word):
        """ Removes the given word from the runtime dictionary """
        self._added_words.discard(word)
        self._added_words_w_affix.pop(word, None)
        self._removed_words.add(word)
        self.h.remove(word)

    def blacklist(self, word):
        """ Removes the given word from the runtime output (not from the dictionary) """
        self._added_words.discard(word)
        self._added_words_w_affix.pop(word, None)
        self._removed_words.add(word)

    def _filter_blacklisted_output(self, words):
        return [word for word in words if word not in self._removed_words]

    def _filter_blacklisted_input(self, word, res):
        if word not in self._removed_words:
            return res
        return []

    def stem(self, word):
        """ Stemmer method. """
        # One can remove() the stem with all forms, but can not remove() a form without removing the stem.
        return self._filter_blacklisted_input(word, self._decode_list(self.h.stem(word)))

    def analyze(self, word):
        """ Provide morphological analysis for the given word. """
        # One can remove() the stem with all forms, but can not remove() a form without removing the stem.
        return self._filter_blacklisted_input(word, self._decode_list(self.h.analyze(word)))

    def generate(self, word, example=None, flags=None):
        """ Provide morphological generation for the given word. """
        if example is not None and flags is None:
            gen_out = self.h.generate(word, example)
        elif example is None and flags is not None:
            gen_out = self.h.generate2(word, flags)
        else:
            raise ValueError('example XOR flags must be supplied!')

        return self._filter_blacklisted_output(self._decode_list(gen_out))

    def spell(self, word):
        """ Checks the spelling of the given word. """
        # One can remove() the stem with all forms, but can not remove() a form without removing the stem.
        return self._filter_blacklisted_input(word, self.h.spell(word))

    def suggest(self, word):
        """ Provide suggestions for the given word. """
        return self._filter_blacklisted_output(self.h.suggest(word))
