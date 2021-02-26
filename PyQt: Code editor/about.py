from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        self.resize(300, 200)

        title = QLabel('Intelligent code \n\nBy:\n')
        title.setAlignment(Qt.AlignCenter)

        author = QLabel('Amey\n')
        author.setAlignment(Qt.AlignCenter)

        message = QLabel('An intelligent code editor for professional and amateur programmers\n')

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(title)
        self.layout.addWidget(author)
        self.layout.addWidget(message)

        self.setLayout(self.layout)