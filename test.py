import fasten
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QMainWindow 
from PyQt5.QtWidgets import QAction, QFileDialog, QTextEdit
from PyQt5.QtGui import QIcon


class FEWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('002-folder.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open file for translate')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 450, 300)
        self.center()
        self.setWindowTitle('Fast English: Английский для ленивых отличников')
        self.setWindowIcon(QIcon('book.png'))
        self.show()

    def center(self):
        main_window = self.frameGeometry()
        mon = QDesktopWidget().availableGeometry().center()
        main_window.moveCenter(mon)
        self.move(main_window.topLeft())   

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]

        
        try:
            document = read_text(path)
        except FileNotFoundError:
            text = 'Некорректный путь или неправильное имя файла.\
            Внимание! В имени файла не должно быть пробелов!'
        except TypeError:
            text = 'Произошла ошибка при чтении файлаю. Возможно, неправильный формат файла(\
            требуется txt) или неправильный путь к файлу. Замените обратный слеш на прямой'
        except:
            text = 'Ошибка. Попробуйте еще раз.'

        try:
            list_word = make_good_word(document)
        except:
            text = 'Ошибка. Некорректное содержимое файла'

        except:
            text = 'Упс. Что-то пошло не так. Попробуете снова?'
        self.textEdit.setText(text)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    fe_window = FEWindow()
    sys.exit(app.exec_())