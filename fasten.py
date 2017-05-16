import os.path
import codecs 
import requests
import config
import sys



class FileCreateException(Exception):
	def __init__(self):
		Exception.__init__(self)


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


def make_translate(list_word):

	articles = []

	for word in list_word:

		temp_dict = {}

		url = '{domain}/dicservice.json/lookup?key={key}&lang=en-ru&text={text}&ui={ui}'.format(
			domain='https://dictionary.yandex.net/api/v1',
			text=word,
			key=config.api_key_for_dictionary,
			ui='ru'
			)

		responce = requests.get(url).json()
		temp_dict['word'] = responce['def'][0]['text']
		count = 0
		temp_list = []
		temp_dict['pos'] = responce['def'][0]['pos']
		temp_dict['tr'] = responce['def'][0]['tr'][0]['text']

		for i in responce['def']:

			if temp_dict['pos'].find(i['pos']) < 0:
				temp_dict['pos'] += ', ' + i['pos']

			for n in i['tr']:
				if temp_dict['tr'].find(n['text']) < 0:
					temp_dict['tr'] += ', ' + n['text']
				try:
					for index in range(len(n['syn'])):
						temp_dict['tr'] += ', ' + n['syn'][index]['text']
				except:
					pass
		
		articles.append(temp_dict)

	return articles


def create_file(path, articles):

	path = os.path.split(path)
	new_name = path[1].split('.')
	new_path = path[0] + '/' + new_name[0] + '_english_words.' + new_name[1]
	n = 1
	flag = 0

	if os.path.isfile(new_path) == True:
		new_attempt = new_path.split('.') 
		temp_path = new_attempt[0] + str(n) + '.' + new_attempt[1]
		n += 1
		flag = 1

	if flag == 1: 
		new_path = temp_path

	file = open(new_path, 'w')
	try:
		for art in articles:
			word = art['word']
			pos = art['pos']
			tr = art['tr']
			temp_str = str(word) + '(' + str(pos) + '): ' + str(tr)
			file.write(temp_str + '\n')
	except:
		return FileCreateException
	finally:
		file.close()

	return new_path


def full_translate(path):

	try:
		document = read_text()
	except FileNotFoundError:
		str_error = 'Некорректный путь или неправильное имя файла'
		return str_error
	except TypeError:
		str_error = 'К сожалению, формат Вашего файла не подходит. Требуется txt'
		return str_error
	except:
		str_error = 'Ошибка. Попробуйте еще раз.'
		return str_error

	try:
		list_word = make_good_word(document)
	except:
		str_error = 'Ошибка. Некорректное содержимое файла'
		return str_error

	try:
		articles = make_translate(list_word) 
	except:
		str_error = 'Ошибка перевода. Возможно, отсутствует подключение. Проверьте подключение и \
				попробуйте еще раз'
		return str_error

	try:
		create_file(articles)
	except FileCreateException:
		str_error = 'Ошибка создания файла. Попробуйте еще раз.'
		return str_error

	return True


if __name__ == '__main__':
	_, path = sys.argv
	translate = full_translate(path)
	if type(translate) == str:
		print(translate)

