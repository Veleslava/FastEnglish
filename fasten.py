import os.path
import codecs 
'''from docx import Document '''


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
		
	'''	elif os.path.splitext(path)[1] == '.doc' or os.path.splitext(path)[1] == '.docx':
		file = codecs.open(path, encoding='utf-8', mode='r')
		document = Document(file)
		file.close()'''
	list_word = []

	for word in document.split():
		word_upper = word.upper()
		if ord(word_upper[0]) > 90 or ord(word_upper[0]) < 65:
			word = word[1:]
		if ord(word_upper[-1]) > 90 or ord(word_upper[-1]) < 65:
			word = word[:-1]
		list_word.append(word)

	return list_word

