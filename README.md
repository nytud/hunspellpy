# HunspellPy
A wrapper and REST API implemented in Python for ___Hunspell__ spellchecker and morphological analyzer_ 

## Requirements

  - _libhunspell-dev_: On Ubuntu 18.04 LTS or higher just `sudo apt install libhunspell-dev`
  - A dictionary package, eg. _hunspell-hu_: On Ubuntu 18.04 LTS or higher just `sudo apt install hunspell-hu`
  - Python 3 (>=3.5, tested with 3.6)
  - Pip to install the additional requirements in requirements.txt
  - (Optional) a cloud service like [Heroku](https://heroku.com) for hosting the API

## Features
 - Spellchecking, stemming and returning the detailed morphological analyses with the proper .dic and .aff files
 - Handling of removing individual words from the dictionary (if a word is added with affixes affixed words could not be removed) 
 - Can be used through REST API, or from Python as a library (see usage examples below)

## Install on local machine

  - Clone the repository
  - Run: `sudo pip3 install -r requirements.txt`
  - Use from Python

## Install to Heroku

  - Register
  - Download Heroku CLI
  - Login to Heroku from the CLI
  - Create an app
  - Clone the repository
  - Add Heroku as remote origin
  - Add APT buildpack: `heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt`
  - Add Python buildpack: `heroku buildpacks:add --index 2 heroku/python`
  - Push the repository to Heroku
  - Enjoy!

## Usage

  - From browser or anyhow through the REST API:
     - Lemmatization: https://hunspellpy.herokuapp.com/stem/működik
     - Detailed analysis: https://hunspellpy.herokuapp.com/analyze/működik
     - Spellcheck: https://hunspellpy.herokuapp.com/spell/működik
     - Lemmatisation with the corresponding detailed analysis: https://hunspellpy.herokuapp.com/dstem/működik
     - The library also support HTTP POST requests to handle multiple words at once. (See examples for details.)

	```python
	>>> import requests
	>>> import json
	>>> word = 'működik'
	>>> json.loads(requests.get('https://hunspellpy.herokuapp.com/spell/' + word).text)[word]
	{'spell': True}
	>>> json.loads(requests.get('https://hunspellpy.herokuapp.com/stem/' + word).text)[word]
	{'stem': ['működik']}
	>>> json.loads(requests.get('https://hunspellpy.herokuapp.com/analyze/' + word).text)[word]
	{'anas': [[['st', 'működik'], ['po', 'vrb'], ['ts', 'PRES_INDIC_INDEF_SG_3']]]}
	>>> json.loads(requests.get('https://hunspellpy.herokuapp.com/dstem/' + word).text)[word]
    {'stem': ['működik'], 'anas': [[['st', 'működik'], ['po', 'vrb'], ['ts', 'PRES_INDIC_INDEF_SG_3']]], 'spell': True}
	>>> words = '\n'.join(('form', word, 'word2', ''))  # One word per line (first line is header, trailing newline is needed!)
	>>> words_out = requests.post('https://hunspellpy.herokuapp.com/spell', files={'file': words}).text.split('\n')
	>>> print(words_out[1].split('\t'))
	['működik', '{"spell": true}']
	>>> words_out = requests.post('https://hunspellpy.herokuapp.com/stem', files={'file': words}).text.split('\n')
	>>> print(words_out[1].split('\t'))
	['működik', '{"stem": ["működik"]}']
	>>> words_out = requests.post('https://hunspellpy.herokuapp.com/analyze', files={'file': words}).text.split('\n')
	>>> print(words_out[1].split('\t'))
	['működik', '{"anas": [[["st", "működik"], ["po", "vrb"], ["ts", "PRES_INDIC_INDEF_SG_3"]]]}']
    >>> words_out = requests.post('https://hunspellpy.herokuapp.com/dstem', files={'file': words}).text.split('\n')
	>>> print(words_out[1].split('\t'))
	['működik', 'true', '{"stem": ["működik"], "anas": [[["st", "működik"], ["po", "vrb"], ["ts", "PRES_INDIC_INDEF_SG_3"]]]}']
	```
 
  - From Python:

	```python
	>>> import hunspellpy.hunspellpy as hunspell
	>>> h = hunspell.HunspellPy()
	>>> h.spell('működik')    # Returns if word spelleed corretly or not?
	True
	>>> h.stem('működik')     # Returns list of stem
	['működik']
	>>> h.analyze('működik')  # Returns list of detailed analyzes
	[' st:működik po:vrb ts:PRES_INDIC_INDEF_SG_3']
	>>> h.dstem('működik')    # Returns list of lemmatisations with the corresponding detailed analyzes (stem, tag and detailed analyzes triples)
	{'anas': [[('st', 'működik'), ('po', 'vrb'), ('ts', 'PRES_INDIC_INDEF_SG_3')]], 'stem': ['működik'], 'spell': True}
	>>> # Add new word to the lexicon
	>>> h.add('működik')
	>>> # Add new word with paradigm (from example) to the lexicon
	>>> h.add('zsíííír', example='zsír')
	>>> # Remove word from the lexicon (with paradigm)
	>>> h.remove('zsíííír')
	>>> # Remove word from the runtime (!) lexicon (without paradigm)
	>>> h.blacklist('zsíííír')
	>>> h.generate('körte', example='almával')
	['körtéjével', 'körtével']
	>>> h.generate('dolgozhat', flags=' st:működik po:vrb ts:PRES_INDIC_INDEF_SG_3')
	['dolgoz', 'dolgozik', 'dolgoz']
	>>> h.suggest('amla')
	['alma', 'ama', 'akla', 'ampa', 'aula', 'pamlag']
	>>> h.add_dic('.../extra.dic')
	>>> h.get_dic_encoding()
	'UTF-8'
	```

## License

This Python wrapper (around pyhunspell package) is licensed under the LGPL 3.0 license.
xtsv, PyHunspell, Hunspell and the dictionaries has their own license.
