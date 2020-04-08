#!/usr/bin/env pyhton3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from . import HunspellPy

from xtsv import build_pipeline, parser_skeleton, jnius_config, add_bool_arg


def print_assert(msg, fun_res, exp_res):
    print(msg, fun_res)
    assert fun_res == exp_res, 'assertion error {0} != {1}'.format(fun_res, exp_res)


def test():
    h = HunspellPy()

    # h.add_dic('extra_words.dic')
    print_assert('OOV analyze(zsíííír):', h.analyze('zsíííír'), [])
    h.add('zsíííír')
    print_assert('OOV added analyze(zsíííír):', h.analyze('zsíííír'), [' st:zsíííír'])
    print_assert('OOV analyze(zsííírral):', h.analyze('zsííírral'), [])
    h.add('zsííír', 'zsír')
    print_assert('OOV added analyze(zsííírral):', h.analyze('zsííírral'), [' st:zsííír is:INSTR'])
    print_assert('analyze(almával):', h.analyze('almával'), [' st:alom po:noun ts:PLUR ts:NOM is:POSS_SG_3 is:INSTR',
                                                             ' st:alma po:noun ts:NOM is:INSTR'])
    print_assert('stem(fúrógéppel):', h.stem('fúrógéppel'), ['fúrógép'])
    print_assert('Generate from ex generate(körte, almátokkal):', h.generate('körte', 'almátokkal'), ['körtétekkel'])
    print_assert('Generate from morph desc '
                 'generate(körte, flags= st:alom po:noun ts:PLUR ts:NOM is:POSS_SG_3 is:INSTR):',
                 h.generate('körte', flags=' st:alom po:noun ts:PLUR ts:NOM is:POSS_SG_3 is:INSTR'), ['körtéjével'])
    print_assert('Dictionary encoding get_dic_encoding():', h.get_dic_encoding(), 'UTF-8')
    h.remove('zsíííír')
    print_assert('OOV removed analyze(zsíííír):', h.analyze('zsíííír'), [])
    print('OOV w affix in the dictionary analyze(zsííírnak):', h.analyze('zsííírnak'), [' st:zsííír is:DAT'])
    h.remove('zsííírnak')
    print_assert('OOV w affix removed analyze(zsííírnak):', h.analyze('zsííírnak'), [])
    print_assert('OOV w other affix still in the dictionary analyze(zsííírral):', h.analyze('zsííírral'),
                 [' st:zsííír is:INSTR'])
    h.remove('zsííír')
    print_assert('OOV w other affix still in the dictionary analyze(zsííírt):', h.analyze('zsííírt'),
                 [' st:zsííír is:ACC'])

    print_assert('Spell spell(almákkkaal):', h.spell('almákkkaal'), False)
    print_assert('Suggest suggest(medvelövő):', h.suggest('medvelövő'), ['medve-lövő', 'medvelóvő', 'medvelövő',
                                                                         'medvelövőt', 'medvelövőn', 'medvelövők',
                                                                         'medvelövői', 'medvelövőé', 'medvelövőd',
                                                                         'medvelövőm', 'melegkedvelő'])
    print_assert('Analyze analyze(lealmáz):', h.analyze('lealmáz'),
                 ['ip:PREF sp:le  st:alma po:noun ts:NOM ds:z_ACTION_vrb ts:PRES_INDIC_INDEF_SG_3'])
    h.add('lebölcsészez', 'lealmáz')
    print_assert('Analyze analyze(lebölcsészezte):', h.analyze('lebölcsészezte'),
                 ['ip:PREF sp:le  st:bölcsész po:noun ts:NOM ds:z_ACTION_vrb ts:PRES_INDIC_INDEF_SG_3 '
                  'is:PAST_INDIC_DEF_SG_3'])
    print_assert('Analyze analyze(portalaníttathat):', h.analyze('portalaníttathat'),
                 [' st:portalanít po:vrb ts:PRES_INDIC_INDEF_SG_3 ds:tAt_FACTITIVE_vrb_tr is:hAt_MODAL_vrb '
                  'ts:PRES_INDIC_INDEF_SG_3'])
    print_assert('Analyze analyze(is):', h.analyze('is'), [' st:is po:con'])
    inp_sen = [['Az'], ['árvíztűrő'], ['tükörfúrógéppel'], ['megcsinált'], ['munkálatok'], ['nehezek'], ['.']]
    exp_sen = [['Az', 'true', '{"anas": [[["st", "az"], ["po", "noun_pron"], ["ts", "NOM"], ["al", "azé"], '
                              '["al", "azzá"], ["al", "azzal"], ["al", "azt"], ["al", "azon"], ["al", "azok"], '
                              '["al", "avval"], ["al", "annál"], ["al", "annak"], ["al", "ahhoz"], ["al", "abból"], '
                              '["al", "abban"], ["al", "abba"]], [["st", "az"], ["po", "det_def"], ["al", "azé"], '
                              '["al", "azzá"], ["al", "azzal"], ["al", "azt"], ["al", "azon"], ["al", "azok"], '
                              '["al", "avval"], ["al", "annál"], ["al", "annak"], ["al", "ahhoz"], ["al", "abból"], '
                              '["al", "abban"], ["al", "abba"]]], "stem": ["az"]}'],
               ['árvíztűrő', 'true', '{"anas": [[["pa", "ár"], ["st", "ár"], ["po", "noun"], ["ts", "NOM"], '
                                     '["al", "árak"], ["pa", "víz"], ["st", "víz"], ["po", "noun"], ["ts", "NOM"], '
                                     '["al", "vizek"], ["pa", "tűrő"], ["st", "tűr"], ["po", "vrb"], '
                                     '["ts", "PRES_INDIC_INDEF_SG_3"], ["al", "tűret"], ["ds", "Ó_PRESPART_adj"], '
                                     '["ts", "NOM"]], [["pa", "árvíz"], ["st", "árvíz"], ["po", "noun"], '
                                     '["ts", "NOM"], ["al", "árvizek"], ["pa", "tűrő"], ["st", "tűr"], ["po", "vrb"], '
                                     '["ts", "PRES_INDIC_INDEF_SG_3"], ["al", "tűret"], ["ds", "Ó_PRESPART_adj"], '
                                     '["ts", "NOM"]]], "stem": ["árvíztűrő"]}'],
               ['tükörfúrógéppel', 'true', '{"anas": [[["pa", "tükör"], ["st", "tükör"], ["po", "noun"], '
                                           '["ts", "NOM"], ["al", "tükrök"], ["pa", "fúrógéppel"], ["st", "fúrógép"], '
                                           '["po", "noun"], ["ts", "NOM"], ["is", "INSTR"]]],'
                                           ' "stem": ["tükörfúrógép"]}'],
               ['megcsinált', 'true', '{"anas": [[["st", "megcsinált"], ["po", "adj"], ["ts", "NOM"]], '
                                      '[["ip", "PREF"], ["sp", "meg"], ["st", "csinál"], ["po", "vrb"], '
                                      '["ts", "PRES_INDIC_INDEF_SG_3"], ["is", "PAST_INDIC_INDEF_SG_3"]], '
                                      '[["ip", "PREF"], ["sp", "meg"], ["st", "csinál"], ["po", "vrb"], '
                                      '["ts", "PRES_INDIC_INDEF_SG_3"], ["ds", "tt_PASTPART_adj"], ["ts", "NOM"]]], '
                                      '"stem": ["megcsinált", "megcsinál"]}'],
               ['munkálatok', 'true', '{"anas": [[["st", "munkálat"], ["po", "noun"], ["ts", "NOM"], ["is", "PLUR"], '
                                      '["is", "NOM"]]], "stem": ["munkálat"]}'],
               ['nehezek', 'true', '{"anas": [[["st", "nehéz"], ["po", "adj"], ["ts", "PLUR"], ["ts", "NOM"]]], '
                                   '"stem": ["nehéz"]}'],
               ['.', 'true', '{"anas": [[["st", "."], ["po", "punct"]]], "stem": ["."]}']]
    print_assert('process_sentence(inp_sen, [0]):', h.process_sentence(inp_sen, [0]), exp_sen)


def input_wrapper():  # TODO: Include in xtsv?
    while True:
        try:
            inp_str = input('--> ')
            if len(inp_str) == 0:
                raise EOFError
            yield inp_str
        except EOFError:
            return


def raw_dstem_helper(fh):
    emmorph = HunspellPy()
    for line in fh:
        line = line.strip()
        for i in emmorph.dstem(line):
            if len(i) == 5:
                print(line, i[2], i[0], i[1], sep='\t')
            else:
                print(line, '<unknown>', sep='\t')
        print()


def raw_input_processor(inp_stream):
    if inp_stream == sys.stdin:
        print('Type one word per line, Ctrl+D or empty word to exit')
        raw_dstem_helper(input_wrapper())
    else:
        raw_dstem_helper(inp_stream)


def main():
    argparser = parser_skeleton(description='Hunspell integrated with the xtsv framework')
    add_bool_arg(argparser, 'raw', 'Process tokens raw one token per line (without xtsv) incl. interactive mode')
    add_bool_arg(argparser, 'test', 'Run predefined test')

    opts = argparser.parse_args()

    if opts.test:
        test()
        exit()

    if opts.raw:
        raw_input_processor(opts.input_stream)
        exit()

    jnius_config.classpath_show_warning = opts.verbose  # Suppress warning.
    conll_comments = opts.conllu_comments

    # Set input and output iterators...
    if opts.input_text is not None:
        input_data = opts.input_text
    else:
        input_data = opts.input_stream
    output_iterator = opts.output_stream

    # Set the tagger name as in the tools dictionary
    used_tools = ['spell']
    presets = []

    # Init and run the module as it were in xtsv

    # The relevant part of config.py
    hunspellpy = ('hunspellpy.hunspellpy', 'HunspellPy', 'HunspellPy', (),
                  {'source_fields': {'form'}, 'target_fields': ['spell', 'hunspell_anas']})
    tools = [(hunspellpy, ('spell', 'hunspell'))]

    # Run the pipeline on input and write result to the output...
    output_iterator.writelines(build_pipeline(input_data, used_tools, tools, presets, conll_comments))

    # TODO this method is recommended when debugging the tool
    # Alternative: Run specific tool for input (still in emtsv format):
    # output_iterator.writelines(process(input_iterator, inited_tools[used_tools[0]]))

    # Alternative2: Run REST API debug server
    # app = pipeline_rest_api('TEST', inited_tools, presets,  False)
    # app.run()


if __name__ == '__main__':
    main()
