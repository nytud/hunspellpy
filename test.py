#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from hunspellpy import HunspellPy

hunspell = HunspellPy()

for l in open('test/test_words.txt'):
    ret = hunspell.process_token(l.strip())
    if len(ret['anas']) > 0:
        print(l.strip(), ret['spell'], ret['stem'], ret['anas'], sep='\t')
    else:
        print(l.strip(), '<unknown>', sep='\t')
