import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, \
    QTabBar, QFrame, QStackedLayout

from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

print("History: ")


class AddressBar(QLineEdit):

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setWindowTitle("Web Surf")

        self.App()
        self.setBaseSize(1280, 900)

    def App(self):

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.tab_bar = QTabBar(movable=True, tabsClosable=True)
        self.tab_bar.tabCloseRequested.connect(self.CloseTab)
        self.tab_bar.tabBarClicked.connect(self.SwitchTab)

        self.tab_bar.setCurrentIndex(0)
        self.tab_bar.setDrawBase(False)

        self.tabCount = 0
        self.tabs = []

        self.Toolbar = QWidget()
        self.ToolbarLayout = QHBoxLayout()
        self.address_Bar = AddressBar()

        self.AddTabButton = QPushButton("+")
        self.AddTabButton.clicked.connect(self.AddTab)

        self.address_Bar.returnPressed.connect(self.BrowseTo)

        self.BackButton = QPushButton("<-")
        self.BackButton.clicked.connect(self.GoBack)

        self.ForwardButton = QPushButton("->")
        self.ForwardButton.clicked.connect(self.GoForward)

        self.ReloadButton = QPushButton("Reload")
        self.ReloadButton.clicked.connect(self.ReloadPage)

        self.ToolbarLayout.addWidget(self.AddTabButton)
        self.ToolbarLayout.addWidget(self.BackButton)
        self.ToolbarLayout.addWidget(self.ForwardButton)
        self.ToolbarLayout.addWidget(self.ReloadButton)
        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.address_Bar)

        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.tab_bar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)

        self.AddTab()

        self.show()

    def CloseTab(self, i):

        self.tab_bar.removeTab(i)

    def AddTab(self):

        i = self.tabCount

        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)

        self.tabs[i].setObjectName("tab" + str(i))

        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("http://www.bing.com"))

        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.SetTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.SetTabContent(i, "url"))

        self.tabs[i].layout.addWidget(self.tabs[i].content)

        self.tabs[i].setLayout(self.tabs[i].layout)

        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        self.tab_bar.addTab("Add New")
        self.tab_bar.setTabData(i, {"object": "tab" + str(i), "initial": i})
        self.tab_bar.setCurrentIndex(i)

        self.tabCount += 1

    def SwitchTab(self, i):

        if self.tab_bar.tabData(i):
            tab_data = self.tab_bar.tabData(i)["object"]
            tab_content = self.findChild(QWidget, tab_data)
            self.container.layout.setCurrentWidget(tab_content)

            new_url = tab_content.content.url().toString()
            self.address_Bar.setText(new_url)

    def BrowseTo(self):
        text = self.address_Bar.text()
        print(text)

        i = self.tab_bar.currentIndex()
        tab = self.tab_bar.tabData(i)["object"]
        wv = self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url = "https://www.bing.com/search?q=" + text
            else:
                url = "http://" + text

        else:
            url = text

        wv.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, content_type):
        tab_name = self.tabs[i].objectName()

        count = 0
        running = True

        current_tab = self.tab_bar.tabData(self.tab_bar.currentIndex())["object"]

        if current_tab == tab_name and content_type == "url":
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.address_Bar.setText(new_url)
            return False

        while running:
            tab_data_name = self.tab_bar.tabData(count)

            if count >= 10:
                running = False

            if tab_name == tab_data_name["object"]:
                if content_type == "title":

                    new_title = self.findChild(QWidget, tab_name).content.title()
                    self.tab_bar.setTabText(count, new_title)

                elif content_type == "icon":
                    new_icon = self.findChild(QWidget, tab_name).content.icon()
                    self.tab_bar.setTabIcon(count, new_icon)

                running = False

            else:
                count += 1

    def GoBack(self):
        active_index = self.tab_bar.currentIndex()

        tab_name = self.tab_bar.tabData(active_index)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.back()

    def GoForward(self):
        active_index = self.tab_bar.currentIndex()

        tab_name = self.tab_bar.tabData(active_index)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.forward()
        pass

    def ReloadPage(self):
        active_index = self.tab_bar.currentIndex()

        tab_name = self.tab_bar.tabData(active_index)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()

    sys.exit(app.exec_())
