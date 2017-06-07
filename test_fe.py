import unittest
import fasten


class TextTestsFE(unittest.TestCase):

	def test_read_text_docx(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/texts/кейт аткинсон.docx'
		with self.assertRaises(TypeError):
			fasten.read_text(path)

	def test_read_text_wrong_path(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/texts/кейт аткинсон'
		with self.assertRaises(FileNotFoundError):
			fasten.read_text(path)

	def test_read_text_wrong_path_2(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/texts/кейт аткисон.txt'
		with self.assertRaises(FileNotFoundError):
			fasten.read_text(path)

	def test_read_text_empty_document(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/texts/пустой.txt'
		self.assertEqual(fasten.read_text(path), '')

	def test_read_text_txt(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/texts/кейт аткинсон.txt'
		self.assertEqual(fasten.read_text(path), 
			'Mr. and Mrs. Dursley, of number! four, Privet Drive, were proud to say that Mrs')

	def test_make_good_word(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/texts/кейт аткинсон.txt'
		document = fasten.read_text(path)
		self.assertEqual(fasten.make_good_word(document), 
			['Mr','and','Mrs','Dursley','of','number','four','Privet','Drive','were','proud','to','say','that'])


class TestTranslateEF(unittest.TestCase):

	def test_rood_word(self):
		self.assertEqual(fasten.make_rood_word('non-educational'), 'educat')

	def test_translate(self):
		self.assertEqual(fasten.make_translate(['proud', 'son', 'Dursley']), 
									([{'word': 'proud', 'pos': 'прилагательное, причастие', 
									'tr': 'гордый, надменный, высокомерный, самолюбивый, горделивый, великолепный, величавый, ретивый, вздувшийся'},
									{'word': 'son', 'pos':'существительное', 'tr': 'сын, потомок, сынок, выходец'}], ['Dursley']))


if __name__ == '__main__':
    unittest.main()
