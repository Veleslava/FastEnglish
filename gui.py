import fasten
import sys
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QMainWindow, QAction
from PyQt5.QtGui import QIcon


class FEWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(app.quit)

        menubar = QMainWindow().menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exitAction)
        self.set_status_bar()

        self.resize(450, 300)
        self.center()
        self.setWindowTitle('Fast English: Английский для ленивых отличников')
        self.setWindowIcon(QIcon('book.png'))
        self.show()

    def center(self):
        main_window = self.frameGeometry()
        mon = QDesktopWidget().availableGeometry().center()
        main_window.moveCenter(mon)
        self.move(main_window.topLeft()) 

    def set_status_bar(self):
        return QMainWindow().statusBar()        


if __name__ == '__main__':

    app = QApplication(sys.argv)

    fe_window = FEWindow()
    sys.exit(app.exec_())