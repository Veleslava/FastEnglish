import os.path
import codecs 
import requests
import config


def read_text(path):
	'''This function separates words. Only txt file!'''
	if os.path.isfile(path) != True:
		raise FileNotFoundError

	if os.path.splitext(path)[1] == '.txt':
		file = codecs.open(path, encoding='utf-8', mode='r')
		document = file.read()
		file.close()
	else:
		raise TypeError
		
	return document


def make_good_word(document):
	'''This function prepares words to translate'''
	list_word = []

	for word in document.split():
		word_upper = word.upper()
		if ord(word_upper[0]) > 90 or ord(word_upper[0]) < 65:
			word = word[1:]
		if ord(word_upper[-1]) > 90 or ord(word_upper[-1]) < 65:
			word = word[:-1]
		if list_word.count(word) == 0:
			list_word.append(word)

	return list_word


def make_post_for_translate(list_word):

	articles = []

	for word in list_word:

		url = '{domain}/dicservice.json/lookup?key={key}&lang=en-ru&text={text}&ui={ui}'.format(
			domain='https://dictionary.yandex.net/api/v1',
			text=word,
			key=config.api_key_for_dictionary,
			ui='ru'
			)

		responce = requests.get(url).json()
		
		articles.append(responce)

	return articles


#print(make_good_word(read_text('C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон.txt')))
print(make_post_for_translate(['proud']))