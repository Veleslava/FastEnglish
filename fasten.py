import os.path
import codecs 
import requests
import config
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, String, Integer, Date, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
import threading
from datetime import datetime


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


class History(Base):
	__tablename__ = 'history'
	id = Column(Integer, primary_key = True)
	path = Column(String)
	date = Column(Date)
	time = Column(Time)
	count_request = Column(Integer)
	execution = Column(Boolean)


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
	count_request = 0

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
			count_request += 1

		else:
			point = s.query(Word).filter(Word.full_word==word).all()[0]
			point.count_translate += 1
			s.commit()
			temp_dict['word'] = point.full_word
			temp_dict['pos'] = point.part_of_speech
			temp_dict['tr'] = point.translate
			articles.append(temp_dict)

	return articles, error_words, count_request


def create_file(path, articles):

	path = os.path.split(path)
	new_name = path[1].split('.')
	new_path = path[0] + '/' + new_name[0] + '_english_words.' + new_name[1]
	n = 1

	while os.path.isfile(new_path) == True:
		new_attempt = new_path.split('.') 
		n += 1
		new_path = new_attempt[0] + str(n) + '.' + new_attempt[1]

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


def word_translate():
	count_request = 0

	words = input('Введите ваши слова через запятую.')
	while words != '0':
		try:
			list_word = [i for i in words.split(',')]
		except:
			print('Упс, что-то пошло не так. Попробуйте еще раз. Для выхода введите 0.')
			words = input()
		translate, error_words, count = make_translate(list_word)
		for i in translate:
			print(i)
		words = input('Вы можете ввести новые слова. Если вы хотите выйти введите 0.')
		if len(error_words) != 0:
			for a in error_words:
				print(a)
		count_request += count

	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()
	time = datetime.time(datetime.today())
	date = datetime.date(datetime.today())

	record = History(count_request=count_request, path=path, execution=True, time=time, date=date)
	s.add(record)
	s.commit()

	return translate, error_words


def smart_translate(list_word):
	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()
	list_word_for_translate = []

	for word in list_word:
		#query = s.query(Word).filter(Word.full_word==word).all()
		#if not query or query[0].count_translate <= 3:
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

	return list_word_for_translate

	
def manual_translate(list_word):

	print('Сейчас вам будут предложены слова из текста. Выберите те из них, которые вы хотите перевести.\
		Введите 1, если вам нужен перевод этого слова, и 0, вы уже его знаете.')

	new_list_word = []

	for word in list_word:
		flag = input(word)
		if flag == '1':
			new_list_word.append(word)

	return new_list_word


def text_to_list(path):
	try:
		document = read_text(path)
	except FileNotFoundError:
		str_error = 'Некорректный путь или неправильное имя файла.\
		Внимание! В имени файла не должно быть пробелов!'
		return str_error
	except TypeError:
		str_error = 'Произошла ошибка при чтении файлаю. Возможно, неправильный формат файла\
		(требуется txt) или неправильный путь к файлу. '
		return str_error
	except:
		str_error = 'Ошибка. Попробуйте еще раз.'
		return str_error

	try:
		list_word = make_good_word(document)
	except:
		str_error = 'Ошибка. Некорректное содержимое файла'
		return str_error

	return list_word


def text_to_translate(list_word, path):

	try:
		translate = make_translate(list_word)
		if len(translate) == 3:
			articles = translate[0]
			error_words = translate[1] 
			count_request = translate[2]
	except:
		str_error = 'Ошибка перевода. Возможно, отсутствует подключение. Проверьте подключение и попробуйте еще раз '
		return str_error

	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()

	time = datetime.time(datetime.today())
	date = datetime.date(datetime.today())

	if count_request != 0:
		record = History(count_request=count_request, path=path, execution=True, time=time, date=date)
		s.add(record)
		s.commit()

	try:
		create_file(path=path, articles=articles)
		if len(error_words) != 0:
			print('К сожалению, эти слова не удалось перевести: ')
			for i in error_words:
				print(i)
	except FileCreateException:
		str_error = 'Ошибка создания файла. Попробуйте еще раз. '
		return str_error

	return error_words


def check_time():
	engine = create_engine("sqlite:///dictionary.db")
	Base.metadata.create_all(bind=engine)
	session = sessionmaker(bind=engine)
	s = session()
	
	today = datetime.today()
	today_time = datetime.time(today)
	today_date = datetime.date(today)
	yesterday = today_date.day 
	if yesterday == 1:
		year = today_date.year[2:]
		month = today_date.month - 1
		if today_date.month in [2, 4, 6, 8, 9, 11]:
			day = 31
		elif today_date.month == 3:
			day = 28
		elif today_date.month == 1:
			day = 31
			year = today_date.year - 1
			month = 12
		else:
			day = 30
	else:
		day = yesterday - 1
		month = today_date.month
		year = str(today_date.year)[2:]

	yesterday_day = datetime.strptime('{} {} {}'.format(day, month, int(year)), '%d %m %y')

	count = 0

	if not s.query(History).filter(History.date==today_date).all():
		for i in s.query(History).filter(History.date==today_date).all():
			count = int(i.count_request)

	if not s.query(History).filter(History.date==yesterday_day and History.time <= today_time).all():
		for i in s.query(History).filter(History.date==today_date).all():
			count = int(i.count_request)

	if count < 9600:
		return True, count
	else:
		return False, count


if __name__ == '__main__':

	if check_time == False:
		print('К сожалению, сервис перевода, которым пользуется программа, ограничивает количество запросов в сутки.\
			На данный момент, количество запросов исчерпано. Вы можете попробовать воспользоваться этим приложением или подождать до завтра.\
			Приносим свои извинения за доставленные неудобства. Хотите продолжить?(Введите 1 - да или 0 - нет) ')
		flag = input()
	else:
		flag = 1
		
	if flag == 1:
		command = sys.argv[1]

		if command == 'word':
			word_translate()
		elif command == 'help':
			print('word - перевод одного или нескольких слов')
			print('full - перевод всех слов в тексте, подходит для новичков')
			print('smart - умный перевод слов, подходит тем, кто знаком со словообразованием')
			print('manual - позволяет вам в ручную определить какие слова переводить, подходит для небольших текстов')
		else:
			path = os.path.normcase(input('Введите путь к файлу. '))
			list_word = text_to_list(path)
			if type(list_word) != str:
				if command == 'full':
					translate = text_to_translate(list_word=list_word, path=path)
				elif command == 'smart':
					new_list_word = smart_translate(list_word)
					translate = text_to_translate(list_word=list_word, path=path)
				elif command == 'manual':
					new_list_word = manual_translate(list_word)
					translate = text_to_translate(list_word=list_word, path=path)
				if type(translate) == str:
					print(translate)
				else:
					print('Перевод завершен')
			else:
				print(list_word)

		