# HunspellPy
A wrapper and REST API implemented in Python for ___Hunspell__ spellchecker and morphological analyzer_ 

This branch can be used for deploying the application to herkou. See [master branch](https://github.com/dlt-rilmta/emmorphpy/tree/master) for other information

__WARNING: Hunspell 1.6.2 (Ubuntu 18.04 Bionic) is broken! It yields UnicodeDecodeError occasionally and messes up the analyses of compound words!__

## Install to Heroku

  - Register
  - Download Heroku CLI
  - Login to Heroku from the CLI
  - Create an app
  - Clone the repository
  - Add Heroku as remote origin
  - Add APT buildpack: `heroku buildpacks:add --index 1 https://github.com/heroku/heroku-buildpack-apt`
  - Add Python buildpack: `heroku buildpacks:add --index 2 heroku/python`
  - Push this branch to Heroku
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

## License

This Python wrapper (around pyhunspell package) is licensed under the LGPL 3.0 license.
xtsv, PyHunspell, Hunspell and the dictionaries has their own license.
