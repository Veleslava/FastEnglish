import unittest
import fasten


class TextTestsFE(unittest.TestCase):

	def test_read_text_docx(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон.docx'
		with self.assertRaises(TypeError):
			fasten.read_text(path)

	def test_read_text_wrong_path(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон'
		with self.assertRaises(FileNotFoundError):
			fasten.read_text(path)

	def test_read_text_wrong_path_2(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткисон.txt'
		with self.assertRaises(FileNotFoundError):
			fasten.read_text(path)

	def test_read_text_empty_document(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/пустой.txt'
		self.assertEqual(fasten.read_text(path), '')

	def test_read_text_txt(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон.txt'
		self.assertEqual(fasten.read_text(path), 
			'Mr. and Mrs. Dursley, of number! four, Privet Drive, were proud to say that Mrs')

	def test_make_good_word(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон.txt'
		document = fasten.read_text(path)
		self.assertEqual(fasten.make_good_word(document), 
			['Mr','and','Mrs','Dursley','of','number','four','Privet','Drive','were','proud','to','say','that'])

	def test_translate(self):
		self.assertEqual(fasten.make_translate(['proud', 'son']), 
			[{'word': 'proud', 'pos': 'прилагательное, причастие', 
			'tr': 'гордый, надменный, высокомерный, самолюбивый, горделивый, великолепный, величавый, ретивый, вздувшийся'},
			{'word': 'son', 'pos':'существительное', 'tr': 'сын, потомок, сынок, выходец'}])


if __name__ == '__main__':
    unittest.main()
