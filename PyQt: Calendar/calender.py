from PyQt5.QtWidgets import *

import sys


class window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calender")
        height = 390
        width = 420
        self.setFixedSize(width, height)

        self.UiComponents()
        self.show()

    def UiComponents(self):
        calender = QCalendarWidget(self)
        calender.setGeometry(10, 10, 400, 250)
        push = QPushButton("Next Year", self)
        push.setGeometry(120, 280, 200, 40)
        push.clicked.connect(lambda: NextYear())
        push_2 = QPushButton("Previous year", self)
        push_2.setGeometry(120, 340, 200, 40)
        push_2.clicked.connect(lambda: PreviousYear())

        def NextYear():
            calender.showNextYear()

        def PreviousYear():
            calender.showPreviousYear()


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = window()
    sys.exit(App.exec())
