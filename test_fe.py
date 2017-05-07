import unittest
import fasten



class TextTestsFE(unittest.TestCase):

	def test_read_text_txt(self):
		path = 'C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон.txt'
		self.assertEqual(fasten.read_text(path), 
			['Mr', 'and', 'Mrs', 'Dursley', 'of', 'number', 'four', 
			'Privet', 'Drive', 'were', 'proud', 'to', 'say', 'that'])

	def test_read_text_docx(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон.docx'
		with self.assertRaises(TypeError):
			fasten.read_text(path)


	def test_read_text_wrong_path(self):
		path ='C:/Users/Администратор/Documents/cs102/FastEnglish/кейт аткинсон'
		with self.assertRaises(FileNotFoundError):
			fasten.read_text(path)

class TimeTestEF(unittest.TestCase):
	pass


if __name__ == '__main__':
    unittest.main()
