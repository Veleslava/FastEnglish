import os.path
import codecs 
import requests
import config
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


class FileCreateException(Exception):
	def __init__(self):
		Exception.__init__(self)


Base = declarative_base()
engine = create_engine("sqlite:///dictionary.db")
Base.metadata.create_all(bind=engine)


class Word(Base):
	__tablename__ = "words"
	id = Column(Integer, primary_key = True)
	full_word = Column(String)
	root_word = Column(String)
	translate = Column(String)
	count_translate = Column(Integer)
	part_of_speech = Column(String)


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


def make_rood_word(word):
	for i in config.prefix:
		pref = word.find(i)
		if pref == 0:
			if word[len(i)] == '-':
				word = word[len(i)+1:]
			else:
				word = word[len(i):]

	for n in config.suffix:
		suf = word.rfind(n)
		if suf != -1:
			word = word[:-len(n)]

	return word


def make_translate(list_word):
	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()
	articles = []
	error_words = []

	for word in list_word:
		temp_dict = {}
		if not s.query(Word).filter(Word.full_word==word).all():
			
			url = '{domain}/dicservice.json/lookup?key={key}&lang=en-ru&text={text}&ui={ui}'.format(
				domain='https://dictionary.yandex.net/api/v1',
				text=word,
				key=config.api_key_for_dictionary,
				ui='ru'
				)

			responce = requests.get(url).json()
			try:
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
				new = Word(full_word=temp_dict['word'], root_word=make_rood_word(word), 
							translate=temp_dict['tr'], count_translate=1,
							part_of_speech=temp_dict['pos'])
				s.add(new)
				s.commit()
			except:
				error_words.append(word)
			
		else:
			point = s.query(Word).filter(Word.full_word==word).all()[0]
			point.count_translate += 1
			s.commit()
			temp_dict['word'] = point.full_word
			temp_dict['pos'] = point.part_of_speech
			temp_dict['tr'] = point.translate
			articles.append(temp_dict)

	return articles, error_words


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
		document = read_text(path)
	except FileNotFoundError:
		str_error = 'Некорректный путь или неправильное имя файла.\
		Внимание! В имени файла не должно быть пробелов!'
		return str_error
	except TypeError:
		str_error = 'Произошла ошибка при чтении файлаю. Возможно, неправильный формат файла(\
		требуется txt) или неправильный путь к файлу. Замените обратный слеш на прямой'
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
		articles, error_words = make_translate(list_word) 
	except:
		str_error = 'Ошибка перевода. Возможно, отсутствует подключение. Проверьте подключение и \
				попробуйте еще раз'
		return str_error

	try:
		create_file(path=path, articles=articles)
		if len(error_words) != 0:
			print('К сожалению, эти слова не удалось перевести: ')
			for i in error_words:
				print(i)
	except FileCreateException:
		str_error = 'Ошибка создания файла. Попробуйте еще раз.'
		return str_error

	return error_words


def word_translate():

	words = input('Введите ваши слова через запятую.')
	while words != '0':
		try:
			list_word = [i for i in words.split(',')]
		except:
			print('Упс, что-то пошло не так. Попробуйте еще раз. Для выхода введите 0.')
			words = input()
		translate, error_words = make_translate(list_word)
		for i in translate:
			print(i)
		words = input('Вы можете ввести новые слова. Если вы хотите выйти введите 0.')
		if len(error_words) != 0:
			for a in error_words:
				print(a)
	return translate, error_words


def smart_translate(path):
	'''Слово проверяется в бд. Если оно там есть и переводилось менее 3 раз, то добавляется в общий словарь. Если
	нет, то удаляются приставки, словоформы и т.д. и проверяется по оставшейся части, если находится несколько слов (более 3)
	с таким корнем, то перевод не производится'''
	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()
	try:
		document = read_text(path)
	except FileNotFoundError:
		str_error = 'Некорректный путь или неправильное имя файла.\
		Внимание! В имени файла не должно быть пробелов!'
		return str_error
	except TypeError:
		str_error = 'Произошла ошибка при чтении файлаю. Возможно, неправильный формат файла(\
		требуется txt) или неправильный путь к файлу. Замените обратный слеш на прямой'
		return str_error
	except:
		str_error = 'Ошибка. Попробуйте еще раз.'
		return str_error

	try:
		list_word = make_good_word(document)
	except:
		str_error = 'Ошибка. Некорректное содержимое файла'
		return str_error

	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()
	list_word_for_translate = []

	for word in list_word:
		if not s.query(Word).filter(Word.full_word==word).all():
			root_word = make_rood_word(word)
			if not s.query(Word).filter(Word.root_word==root_word).all():
				list_word_for_translate.append(word)
			else:
				point = s.query(Word).filter(Word.root_word==root_word).all()[0]
				if len(point.root_word) <= 3:
					list_word_for_translate.append(word)
		else:
			point = s.query(Word).filter(Word.full_word==word).all()[0].count_translate
			if point <= 3:
				list_word_for_translate.append(word)

	try:
		articles, error_words = make_translate(list_word_for_translate) 
	except:
		str_error = 'Ошибка перевода.'
		return str_error

	try:
		create_file(path=path, articles=articles)
		if len(error_words) != 0:
			print('К сожалению, эти слова не удалось перевести: ')
			for i in error_words:
				print(i)
	except FileCreateException:
		str_error = 'Ошибка создания файла. Попробуйте еще раз.'
		return str_error

	return error_words


def manual_translate(path):
	
	try: 
		document = read_text(path)
	except FileNotFoundError:
		str_error = 'Некорректный путь или неправильное имя файла.\
		Внимание! В имени файла не должно быть пробелов!'
		return str_error
	except TypeError:
		str_error = 'Произошла ошибка при чтении файлаю. Возможно, неправильный формат файла(\
		требуется txt) или неправильный путь к файлу. Замените обратный слеш на прямой'
		return str_error
	except:
		str_error = 'Ошибка. Попробуйте еще раз.'
		return str_error

	try:
		list_word = make_good_word(document)
	except:
		str_error = 'Ошибка. Некорректное содержимое файла'
		return str_error

	print('Сейчас вам будут предложены слова из текста. Выберите те из них, которые вы хотите перевести.\
		Введите 1, если вам нужен перевод этого слова, и 0, вы уже его знаете.')

	new_list_word = []

	for word in list_word:
		flag = input(word)
		if flag == '1':
			new_list_word.append(word)

	try:
		articles, error_words = make_translate(new_list_word) 
	except:
		str_error = 'Ошибка перевода.'
		return str_error

	try:
		create_file(path=path, articles=articles)
		if len(error_words) != 0:
			print('К сожалению, эти слова не удалось перевести: ')
			for i in error_words:
				print(i)
	except FileCreateException:
		str_error = 'Ошибка создания файла. Попробуйте еще раз.'
		return str_error

	return error_words


if __name__ == '__main__':
	 
	command = sys.argv[1]
	if command == 'word':
		word_translate()

	elif command == 'help':
		print('word - перевод одного или нескольких слов')
		print('full - перевод всех слов в тексте, подходит для новичков')
		print('smart - умный перевод слов, подходит тем, кто знаком со словообразованием')
		print('manual - позволяет вам в ручную определить какие слова переводить, подходит для небольших текстов')
	else:
		path = os.path.normcase(r(input('Введите путь к файлу. Используйте прямой слеш')))
		if command == 'full':
			translate = full_translate(path)
		elif command == 'smart':
			translate = smart_translate(path)
		elif command == 'manual':
			translate = manual_translate(path)

		if type(translate) == str:
			print(translate)
