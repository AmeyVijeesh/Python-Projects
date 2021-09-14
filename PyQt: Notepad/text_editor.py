#!/usr/bin/python3
# -- coding: utf-8 --


from PyQt5.QtWidgets import QTextEdit, QWidget,\
    QVBoxLayout, QApplication,QFileDialog, QMessageBox,\
    QHBoxLayout, QToolBar, QComboBox, QAction, QLineEdit,\
    QMenu, QMainWindow, QActionGroup,QFontComboBox, QColorDialog,\
    QInputDialog, QPushButton, QPlainTextEdit

from PyQt5.QtGui import QIcon, QColor, QTextCursor, QKeySequence,\
    QTextCharFormat, QTextCharFormat, QFont, QPixmap, QFontDatabase,\
    QFontInfo, QTextDocumentWriter, QImage, QTextListFormat, QTextBlockFormat,\
    QTextDocumentFragment, QKeyEvent

from PyQt5.QtCore import Qt, QDir, QFile, QFileInfo, QSettings, QTextCodec, QSize

from PyQt5 import QtPrintSupport

import sys

import os

import webbrowser


tab = "\t" # tab
eof = "\n" # end of line

table_header2 = "<table></tr><tr><td>    Column1    </td><td>    Column2    </td></tr></table>"
table_header3 = "<table></tr><tr><td>    Column1    </td><td>    Column2    </td><td>    Column3    </td></tr></table>"


class HTMLEditor(QWidget):


    def __init__(self, parent=None, text=""):
        super(HTMLEditor, self).__init__(parent)

        self.ed = QPlainTextEdit()
        self.btnOK = QPushButton("OK", clicked=self.sendText)
        self.btnCancel = QPushButton("Cancel", clicked=self.cancelAction)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.btnCancel)
        self.hbox.addWidget(self.btnOK)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.ed)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        # self.ed.setPlainText(text)


    def sendText(self):
        return self.ed.toPlainText()


    def cancelAction(self):
        self.close()


class myEditor(QMainWindow):


    def __init__(self, parent=None):
        super(myEditor, self).__init__(parent)

        self.setStyleSheet(myStyleSheet(self))

        self.MaxRecentFiles = 5

        self.windowList = []
        self.recentFileActs = []
        self.mainText = " "

        self.settings = QSettings('Amey Vijeesh', "Amey's Word Processor")

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.editor = QTextEdit()

        self.editor.setStyleSheet(myStyleSheet(self))

        self.editor.setTabStopWidth(14)
        self.editor.setContextMenuPolicy(Qt.CustomContextMenu)
        self.editor.customContextMenuRequested.connect(self.contextMenuRequested)

        self.createActions()
        self.createToolbarActions()

        self.createToolbar()
        self.create_Menubar()


    def createToolbarActions(self):

        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                              statusTip="create a new file",
                              triggered=self.newFile)
        self.newAct.setIcon(QIcon.fromTheme("gtk-new"))

        self.openAct = QAction("&Open", self, shortcut=QKeySequence.Open,
                               statusTip="open file",
                               triggered=self.openFile)
        self.openAct.setIcon(QIcon.fromTheme("gtk-open"))

        self.importRTFAct = QAction(QIcon.fromTheme("gnome-mime-application-rtf"), "import RTF", self,
                                    statusTip="import RTF File",
                                    triggered=self.importRTF)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                               statusTip="save file",
                               triggered=self.fileSave)
        self.saveAct.setIcon(QIcon.fromTheme("gtk-save"))

        self.saveAsAct = QAction("&Save as ...", self,
                                 shortcut=QKeySequence.SaveAs,
                                 statusTip="save file as ...",
                                 triggered=self.fileSaveAs)
        self.saveAsAct.setIcon(QIcon.fromTheme("gtk-save-as"))

        self.saveAsWPSAct = QAction("&Save as WPS office Document", self,
                                    shortcut="Ctrl+Shift+e",
                                    statusTip="save file as WPS Document",
                                    triggered=self.fileSaveAsWPS)
        self.saveAsWPSAct.setIcon(QIcon.fromTheme("libreoffice-writer"))

        self.pdfAct = QAction("export PDF", self,
                              statusTip="save file as PDF",
                              triggered=self.exportPDF)
        self.pdfAct.setIcon(QIcon.fromTheme("application-pdf"))

        #print preview
        self.printPreviewAct = QAction("preview", self,
                                       shortcut=QKeySequence.Print,
                                       statusTip="Preview Document",
                                       triggered=self.handlePrintPreview)
        self.printPreviewAct.setIcon(QIcon.fromTheme("gtk-print-preview"))

        ### print
        self.printAct = QAction("print", self,
                                shortcut=QKeySequence.Print,
                                statusTip="Print Document",
                                triggered=self.handlePrint)
        self.printAct.setIcon(QIcon.fromTheme("gtk-print"))
        ### show in Browser
        self.browserAct = QAction("preview in Browser", self, shortcut="F5",
                                  statusTip="preview in Browser",
                                  triggered=self.handleBrowser)
        self.browserAct.setIcon(QIcon.fromTheme("browser"))

        self.exitAct = QAction("Exit", self,
                               shortcut=QKeySequence.Quit,
                               statusTip="Exit",
                               triggered=self.handleQuit)
        self.exitAct.setIcon(QIcon.fromTheme("application-exit"))

        self.repAllAct = QPushButton("replace all")
        self.repAllAct.setIcon(QIcon.fromTheme("gtk-find-and-replace"))
        self.repAllAct.setStatusTip("replace all")
        self.repAllAct.clicked.connect(self.replaceAll)

        self.bgAct = QAction("change Background Color", self,
                             triggered=self.changeBGColor)
        self.bgAct.setStatusTip("change Background Color")
        self.bgAct.setIcon(QIcon.fromTheme("preferences-color-symbolic"))


    def createToolbar(self):

        ### begin toolbar
        self.file_tb = QToolBar(self)
        self.file_tb.setIconSize(QSize(16, 16))
        self.file_tb.setWindowTitle("File Toolbar")

        self.file_tb.addAction(self.newAct)
        self.file_tb.addAction(self.openAct)

        self.file_tb.addSeparator()

        self.file_tb.addAction(self.saveAct)
        self.file_tb.addAction(self.saveAsAct)

        self.file_tb.addSeparator()

        self.file_tb.addAction(self.saveAsWPSAct)

        self.file_tb.addSeparator()

        self.file_tb.addAction(self.pdfAct)

        self.file_tb.addSeparator()

        self.file_tb.addAction(self.printPreviewAct)
        self.file_tb.addAction(self.printAct)

        self.file_tb.addSeparator()

        self.file_tb.addAction(self.browserAct)

        self.file_tb.addSeparator()

        self.file_tb.addAction(QAction(QIcon.fromTheme('image'), "insert Image", self,
                                       statusTip="insert an image",
                                       triggered=self.insertImage))

        ### find / replace toolbar
        self.edit_tb = QToolBar(self)
        self.edit_tb.setIconSize(QSize(16, 16))
        self.edit_tb.setWindowTitle("Find Toolbar")

        self.findfield = QLineEdit()
        self.findfield.addAction(QIcon.fromTheme("gtk-find"), 0)

        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(200)

        self.findfield.setPlaceholderText("find")
        self.findfield.setStatusTip("press RETURN to find")

        self.findfield.setText("")
        self.findfield.returnPressed.connect(self.findText)
        self.edit_tb.addWidget(self.findfield)

        self.replacefield = QLineEdit()
        self.replacefield.addAction(QIcon.fromTheme("gtk-find-and-replace"), 0)

        self.replacefield.setClearButtonEnabled(True)
        self.replacefield.setFixedWidth(200)

        self.replacefield.setPlaceholderText("replace with")
        self.replacefield.setStatusTip("press RETURN to replace the first")

        self.replacefield.returnPressed.connect(self.replaceOne)

        self.edit_tb.addSeparator()

        self.edit_tb.addWidget(self.replacefield)

        self.edit_tb.addSeparator()

        self.edit_tb.addWidget(self.repAllAct)

        self.edit_tb.addSeparator()

        self.edit_tb.addAction(self.bgAct)

        ### Format Toolbar
        self.format_tb = QToolBar(self)
        self.format_tb.setIconSize(QSize(16, 16))
        self.format_tb.setWindowTitle("Format Toolbar")

        self.actionTextBold = QAction(QIcon.fromTheme('format-text-bold-symbolic'), "&Bold", self,
                                      priority=QAction.LowPriority,
                                      shortcut=Qt.CTRL + Qt.Key_B,
                                      triggered=self.textBold, checkable=True)
        self.actionTextBold.setStatusTip("bold")

        bold = QFont()
        bold.setBold(True)

        self.actionTextBold.setFont(bold)
        self.format_tb.addAction(self.actionTextBold)

        self.actionTextItalic = QAction(QIcon.fromTheme('format-text-italic-symbolic'), "&Italic", self,
                                        priority=QAction.LowPriority,
                                        shortcut=Qt.CTRL + Qt.Key_I,
                                        triggered=self.textItalic, checkable=True)

        italic = QFont()
        italic.setItalic(True)

        self.actionTextItalic.setFont(italic)
        self.format_tb.addAction(self.actionTextItalic)

        self.actionTextUnderline = QAction(QIcon.fromTheme('format-text-underline-symbolic'),
                                           "&Underline", self,
                                           priority=QAction.LowPriority,
                                           shortcut=Qt.CTRL + Qt.Key_U,
                                           triggered=self.textUnderline, checkable=True)

        underline = QFont()
        underline.setUnderline(True)

        self.actionTextUnderline.setFont(underline)
        self.format_tb.addAction(self.actionTextUnderline)

        self.format_tb.addSeparator()

        self.grp = QActionGroup(self, triggered=self.textAlign)


        if QApplication.isLeftToRight():
            self.actionAlignLeft = QAction(QIcon.fromTheme('format-justify-left-symbolic'), "&Left", self.grp)

            self.actionAlignCenter = QAction(QIcon.fromTheme('format-justify-center-symbolic'), "C&enter", self.grp)

            self.actionAlignRight = QAction(QIcon.fromTheme('format-justify-right-symbolic'), "&Right", self.grp)

        else:
            self.actionAlignRight = QAction(QIcon.fromTheme('gtk-justify-right-symbolic'), "&Right", self.grp)

            self.actionAlignCenter = QAction(QIcon.fromTheme('gtk-justify-center-symbolic'), "C&enter", self.grp)

            self.actionAlignLeft = QAction(QIcon.fromTheme('format-justify-left-symbolic'), "&Left", self.grp)


        self.actionAlignJustify = QAction(QIcon.fromTheme('format-justify-fill-symbolic'), "&Justify", self.grp)

        self.actionAlignLeft.setShortcut(Qt.CTRL + Qt.Key_L)

        self.actionAlignLeft.setCheckable(True)
        self.actionAlignLeft.setPriority(QAction.LowPriority)

        self.actionAlignCenter.setShortcut(Qt.CTRL + Qt.Key_E)

        self.actionAlignCenter.setCheckable(True)
        self.actionAlignCenter.setPriority(QAction.LowPriority)

        self.actionAlignRight.setShortcut(Qt.CTRL + Qt.Key_R)

        self.actionAlignRight.setCheckable(True)
        self.actionAlignRight.setPriority(QAction.LowPriority)

        self.actionAlignJustify.setShortcut(Qt.CTRL + Qt.Key_J)

        self.actionAlignJustify.setCheckable(True)
        self.actionAlignJustify.setPriority(QAction.LowPriority)

        self.format_tb.addActions(self.grp.actions())

        # self.indentAct = QAction(QIcon.fromTheme("format-indent-more-symbolic"), "indent more", self,
        # triggered = self.indentLine, shortcut = "F8")
        #        self.indentLessAct = QAction(QIcon.fromTheme("format-indent-less-symbolic"),
        #        "indent less", self, triggered = self.indentLessLine, shortcut = "F9")
        #        self.format_tb.addAction(self.indentAct)
        #        self.format_tb.addAction(self.indentLessAct)

        pix = QPixmap(16, 16)

        pix.fill(Qt.black)

        self.actionTextColor = QAction(QIcon(pix), "TextColor...", self,
                                       triggered=self.textColor)

        self.format_tb.addSeparator()

        self.format_tb.addAction(self.actionTextColor)

        self.font_tb = QToolBar(self)

        self.font_tb.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)

        self.font_tb.setWindowTitle("Font Toolbar")

        self.comboStyle = QComboBox(self.font_tb)

        self.font_tb.addWidget(self.comboStyle)

        self.comboStyle.addItem("Standard")

        self.comboStyle.addItem("Bullet List (Disc)")
        self.comboStyle.addItem("Bullet List (Circle)")
        self.comboStyle.addItem("Bullet List (Square)")

        self.comboStyle.addItem("Ordered List (Decimal)")

        self.comboStyle.addItem("Ordered List (Alpha lower)")
        self.comboStyle.addItem("Ordered List (Alpha upper)")

        self.comboStyle.addItem("Ordered List (Roman lower)")
        self.comboStyle.addItem("Ordered List (Roman upper)")
        self.comboStyle.activated.connect(self.textStyle)

        self.comboStyle.addItem("Standard")

        self.comboStyle.addItem("Bullet List (Disc)")
        self.comboStyle.addItem("Bullet List (Circle)")
        self.comboStyle.addItem("Bullet List (Square)")

        self.comboStyle.addItem("Ordered List (Decimal)")

        self.comboStyle.addItem("Ordered List (Alpha lower)")
        self.comboStyle.addItem("Ordered List (Alpha upper)")

        self.comboStyle.addItem("Ordered List (Roman lower)")
        self.comboStyle.addItem("Ordered List (Roman upper)")

        self.comboStyle.activated.connect(self.textStyle)


        self.comboFont = QFontComboBox(self.font_tb)

        self.font_tb.addSeparator()

        self.font_tb.addWidget(self.comboFont)

        self.comboFont.activated[str].connect(self.textFamily)

        self.comboSize = QComboBox(self.font_tb)

        self.font_tb.addSeparator()

        self.comboSize.setObjectName("comboSize")

        self.font_tb.addWidget(self.comboSize)
        self.comboSize.setEditable(True)

        db = QFontDatabase()

        for size in db.standardSizes():

            self.comboSize.addItem("%s" % size)

        self.comboSize.addItem("%s" % 90)

        self.comboSize.addItem("%s" % 100)

        self.comboSize.addItem("%s" % 160)

        self.comboSize.activated[str].connect(self.textSize)

        self.comboSize.setCurrentIndex(
            self.comboSize.findText(
                "%s" % (QApplication.font().pointSize())
            )
        )

        self.addToolBar(self.file_tb)
        self.addToolBar(self.format_tb)

        self.addToolBar(self.font_tb)


    def importRTF(self):

        self.newFile()
        rtext = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body>""" + '\n'

        btext = """<!--EndFragment--></p></body></html>"""
        path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath() + "/Documents/",
                                              "RTF Files (*.rtf)")


        if path:

            inFile = QFile(path)


            if path.endswith(".rtf"):

                os.system("cd /tmp;libreoffice --headless --convert-to html '" + path + "'")
                newfile = "/tmp/" + self.strippedName(path).replace(".rtf", ".html")


                with open(newfile, 'r') as f:

                    t = f.read().replace(rtext, "").replace(btext, "")

                    self.editor.insertHtml(t.replace(rtext, "").replace(btext, ""))
                    self.setModified(False)

                    all = self.editor.document().toHtml()
                    clipboard = QApplication.clipboard()
                    clipboard.setText(all)

                    # self.setModified(False)

                    self.newFile()
                    self.editor.insertHtml(clipboard.text())
                    self.statusBar().showMessage("File is in '/tmp' *** please use 'save as ...'")

                    # self.setModified(True)"g


    def msgbox(self, title, message):

        QMessageBox.warning(self, title, message)


    def indentLine(self):

        if not self.editor.textCursor().selectedText() == "":

            ot = self.editor.textCursor().selection().toHtml()
            self.msgbox("HTML", str(ot))

    def indentLessLine(self):

        if not self.editor.textCursor().selectedText() == "":

            newline = u"\u2029"

            list = []
            ot = self.editor.textCursor().selectedText()
            theList = ot.splitlines()
            linecount = ot.count(newline)

            for i in range(linecount + 1):

                list.insert(i, (theList[i]).replace(tab, "", 1))

            self.editor.textCursor().insertText(newline.join(list))
            self.setModified(True)


    def create_Menubar(self):

        bar = self.menuBar()

        self.file_menu = bar.addMenu("File")

        self.file_menu.addAction(QIcon.fromTheme("dialog-question"), "About AWP ", self.about,
                                 shortcut="Ctrl+i")
        self.separatorAct = self.file_menu.addSeparator()


        self.file_menu.addAction(self.newAct)

        self.file_menu.addAction(self.openAct)

        self.file_menu.addAction(self.importRTFAct)

        self.file_menu.addAction(self.saveAct)

        self.file_menu.addAction(self.saveAsAct)


        self.file_menu.addSeparator()

        self.file_menu.addAction(self.saveAsWPSAct)

        self.file_menu.addSeparator()

        self.file_menu.addAction(QIcon.fromTheme("application-pdf"), "export PDF", self.exportPDF)

        self.file_menu.addSeparator()

        for i in range(self.MaxRecentFiles):

            self.file_menu.addAction(self.recentFileActs[i])

        self.updateRecentFileActions()

        self.file_menu.addSeparator()

        self.clearRecentAct = QAction("clear Recent Files List", self, triggered=self.clearRecentFiles)
        self.clearRecentAct.setIcon(QIcon.fromTheme("edit-clear"))

        self.file_menu.addAction(self.clearRecentAct)
        self.file_menu.addSeparator()

        self.file_menu.addAction(QAction(QIcon.fromTheme('html'), "get HTML (Document)", self, triggered=self.getHTML))

        self.file_menu.addSeparator()

        self.file_menu.addAction(self.exitAct)

        edit_menu = bar.addMenu("Edit")

        edit_menu.addAction(
            QAction(QIcon.fromTheme('edit-undo'), "Undo", self,
                    triggered=self.editor.undo, shortcut="Ctrl+u"))
        edit_menu.addAction(
            QAction(QIcon.fromTheme('edit-redo'), "Redo", self,
                    triggered=self.editor.redo, shortcut="Shift+Ctrl+u"))

        edit_menu.addSeparator()

        edit_menu.addAction(
            QAction(QIcon.fromTheme('edit-copy'), "Copy", self,
                    triggered=self.editor.copy, shortcut=QKeySequence.Copy))

        edit_menu.addAction(
            QAction(QIcon.fromTheme('edit-cut'), "Cut", self,
                    triggered=self.editor.cut, shortcut=QKeySequence.Cut))

        edit_menu.addAction(QAction(QIcon.fromTheme('edit-paste'), "Paste", self,
                                   triggered=self.editor.paste,
                                   shortcut=QKeySequence.Paste))

        edit_menu.addAction(QAction(QIcon.fromTheme('edit-delete'), "Delete", self,
                                   triggered=self.editor.cut,
                                   shortcut=QKeySequence.Delete))

        edit_menu.addSeparator()

        edit_menu.addAction(
            QAction(QIcon.fromTheme('edit-select-all'), "Select All", self,
                    triggered=self.editor.selectAll,
                    shortcut=QKeySequence.SelectAll))

        edit_menu.addSeparator()

        edit_menu.addAction(QAction(QIcon.fromTheme('edit-copy'), "grab selected line", self,
                                   triggered=self.grabLine))

        edit_menu.addSeparator()

        edit_menu.addAction(QAction(QIcon.fromTheme('image'), "insert Image", self,
                                   triggered=self.insertImage))

        edit_menu.addSeparator()

        edit_menu.addAction(
            QAction(QIcon.fromTheme('input-tablet'), "insert Table (2 Column)", self,
                    triggered=self.insertTable))

        edit_menu.addAction(
            QAction(QIcon.fromTheme('input-tablet'), "insert Table (3 Column)", self,
                    triggered=self.insertTable3))

        edit_menu.addSeparator()

        edit_menu.addAction(
            QAction(QIcon.fromTheme('text-html'), "convert from HTML", self,
                    triggered=self.convertFromHTML,
                    shortcut="F10"))

        edit_menu.addSeparator()

        edit_menu.addAction(QAction(QIcon.fromTheme('browser'), "insert Link", self,
                                   triggered=self.insertLink))

        edit_menu.addAction(QAction(QIcon.fromTheme('browser'), "edit Link", self
                                   , triggered=self.editLink))

        edit_menu.addSeparator()

        edit_menu.addAction(QAction(QIcon.fromTheme('input-tablet'), "edit body style", self,
                                   triggered=self.editBody))

        edit_menu.addSeparator()

        edit_menu.addAction(
            QAction(QIcon.fromTheme('input-tablet'), "edit HTML (selected Text)", self,
                    triggered=self.editHTML))

        edit_menu.addSeparator()

        edit_menu.addAction(QAction(QIcon.fromTheme('stock_calendar'), "insert Date", self,
                                   triggered=self.insertDate))

        edit_menu.addAction(QAction(QIcon.fromTheme('stock_calendar'), "insert Time", self,
                                   triggered=self.insertTime))

        edit_menu.addAction(
            QAction(QIcon.fromTheme('stock_calendar'), "insert Date && Time", self,
                    triggered=self.insertDateTime))

        edit_menu.addSeparator()

        edit_menu.addAction(self.bgAct)

        self.formatMenu = QMenu("&Format", self)

        self.formatMenu.addAction(self.actionTextBold)
        self.formatMenu.addAction(self.actionTextItalic)
        self.formatMenu.addAction(self.actionTextUnderline)

        self.formatMenu.addSeparator()

        self.formatMenu.addActions(self.grp.actions())

        self.formatMenu.addSeparator()

        self.formatMenu.addAction(self.actionTextColor)

        bar.addMenu(self.formatMenu)

        # Laying out...
        layoutV = QVBoxLayout()

        layoutV.addWidget(self.edit_tb)
        layoutV.addWidget(self.editor)
        
        mq = QWidget(self)
        mq.setLayout(layoutV)
        self.setCentralWidget(mq)
        self.statusBar().showMessage("New file - ")

        self.installEventFilter(self)

        self.cursor = QTextCursor()
        self.editor.setTextCursor(self.cursor)

        self.editor.setPlainText(self.mainText)
        self.editor.moveCursor(self.cursor.End)

        self.editor.textCursor().deletePreviousChar()
        self.editor.document().modificationChanged.connect(self.setWindowModified)

        self.extra_selections = []
        self.filename = ""
        self.filename = ""

        self.editor.setFocus()
        self.setModified(False)

        self.fontChanged(self.editor.font())
        self.colorChanged(self.editor.textColor())

        self.alignmentChanged(self.editor.alignment())

        self.editor.document().modificationChanged.connect(
            self.setWindowModified)

        self.setWindowModified(self.editor.document().isModified())
        self.editor.setAcceptRichText(True)

        self.editor.currentCharFormatChanged.connect(
            self.currentCharFormatChanged)

        self.editor.cursorPositionChanged.connect(self.cursorPositionChanged)

    #        QApplication.clipboard().dataChanged.connect(self.clipboardDataChanged)


    def insertDate(self):

        import time
        from datetime import date

        today = date.today().strftime("%A, %d.%B %Y")
        self.editor.textCursor().insertText(today)


    def insertTime(self):

        import time
        from datetime import date

        today = time.strftime("%H:%M Uhr")
        self.editor.textCursor().insertText(today)


    def insertDateTime(self):

        self.insertDate()
        self.editor.textCursor().insertText(eof)
        self.insertTime()
        self.editor.textCursor().insertText(eof)


    def changeBGColor(self):

        all = self.editor.document().toHtml()
        bgcolor = all.partition("<body style=")[2].partition(">")[0].partition('bgcolor="')[2].partition('"')[0]

        if not bgcolor == "":

            col = QColorDialog.getColor(QColor(bgcolor), self)

            if not col.isValid():

                return

            else:
                color_name = col.name()
                new = all.replace("bgcolor=" + '"' + bgcolor + '"', "bgcolor=" + '"' + color_name + '"')
                self.editor.document().setHtml(new)

        else:
            col = QColorDialog.getColor(QColor("#FFFFFF"), self)

            if not col.isValid():

                return

            else:
                all = self.editor.document().toHtml()
                body = all.partition("<body style=")[2].partition(">")[0]

                new_body = body + "background_color=" + '"' + col.name() + '"'

                new = all.replace(body, new_body)
                self.editor.document().setHtml(new)


    def getHTML(self):

        all = self.editor.document().toHtml()
        clipboard = QApplication.clipboard()

        clipboard.setText(all)
        self.statusBar().showMessage("HTML is in clipboard")


    def editHTML(self):

        rich_text = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "https://www.w3.org/TR/REC-html40/strict.dtd://w">
<html><head><meta name="AWP" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body>""" + '\n'

        html_text = """<!--EndFragment--></p></body></html>"""
        all = self.editor.textCursor().selection().toHtml()

        # dlg = QInputDialog(self, Qt.Window)

        # dlg.setOption(QInputDialog.UsePlainTextEditForTextInput, True)
        #
        # new, ok = dlg.getMultiLineText(self, 'change HTML', "edit HTML", all.replace(r_text, ""))
        # if ok:
        #    self.editor.textCursor().insertHtml(new)
        #    self.statusBar().showMessage("HTML changed")
        # else:
        #    self.statusBar().showMessage("HTML not changed")

        self.h_editor = HTMLEditor()

        self.h_editor.ed.setPlainText(all.replace(rich_text, "").replace(html_text, ""))

        self.h_editor.setGeometry(0, 0, 800, 600)

        self.h_editor.show()


    def editBody(self):

        all = self.editor.document().toHtml()
        body = all.partition("<body style=")[2].partition(">")[0]
        dlg = QInputDialog()

        body, ok = dlg.getText(self, 'change body style', "", QLineEdit.Normal, body, Qt.Dialog)

        if ok:
            new = all.replace(body, body)
            self.editor.document().setHtml(new)
            self.statusBar().showMessage("body style changed")

        else:
            self.statusBar().showMessage("body style not changed")


    def insertTable(self):

        self.editor.textCursor().insertHtml(table_header2)

    def insertTable3(self):

        self.editor.textCursor().insertHtml(table_header3)

    def handleBrowser(self):

        if self.editor.toPlainText() == "":

            self.statusBar().showMessage("no text")

        else:

            if not self.editor.document().isModified() == True:

                webbrowser.open(self.filename, new=0, autoraise=True)

            else:
                filename = "/tmp/browser.html"

                writer = QTextDocumentWriter(filename)
                success = writer.write(self.editor.document())

                if success:
                    webbrowser.open(filename, new=0, autoraise=True)

                return success


    def contextMenuRequested(self, point):

        context_menu = QMenu()

        context_menu = self.editor.createStandardContextMenu()

        context_menu.addSeparator()

        context_menu.addAction(QAction(QIcon.fromTheme('edit-copy'), "grab this line", self,
                                triggered=self.grabLine))

        context_menu.addSeparator()

        context_menu.addAction(QAction(QIcon.fromTheme('image-x-generic'), "insert Image", self,
                                triggered=self.insertImage))

        context_menu.addSeparator()

        context_menu.addAction(
            QAction(QIcon.fromTheme('input-tablet'), "insert Table (2 Column)", self,
                    triggered=self.insertTable))

        context_menu.addAction(
            QAction(QIcon.fromTheme('input-tablet'), "insert Table (3 Column)", self,
                    triggered=self.insertTable3))

        context_menu.addSeparator()

        context_menu.addAction(
            QAction(QIcon.fromTheme('text-html'), "convert from HTML", self,
                    triggered=self.convertFromHTML))

        context_menu.addSeparator()

        context_menu.addAction(QAction(QIcon.fromTheme('text-plain'), "convert to Text", self,
                                triggered=self.convertToHTML))

        context_menu.addSeparator()

        context_menu.addAction(QAction(QIcon.fromTheme('browser'), "insert Link", self,
                                triggered=self.insertLink))

        context_menu.addAction(QAction(QIcon.fromTheme('browser'), "edit Link", self,
                                triggered=self.editLink))

        context_menu.addSeparator()

        context_menu.addAction(
            QAction(QIcon.fromTheme('input-tablet'), "edit HTML (selected Text)", self,
                    triggered=self.editHTML))

        context_menu.addSeparator()

        context_menu.addAction(self.bgAct)
        context_menu.exec_(self.editor.mapToGlobal(point))


    def editLink(self):

        if not self.editor.textCursor().selectedText() == "":

            mt = self.editor.textCursor().selectedText()
            text = QTextDocumentFragment.toHtml(self.editor.textCursor().selection())
            url = text.partition('<a href="')[2].partition('">')[0]
            dlg = QInputDialog()

            dlg.setOkButtonText("Change")

            link, ok = dlg.getText(self, 'change URL', "", QLineEdit.Normal, str(url), Qt.Dialog)

            if ok:
                if link.startswith("http"):
                    self.editor.textCursor().insertHtml("<a href='" + link + "' target='_blank'>" + mt + "</a>")
                    self.statusBar().showMessage("link added")

                else:
                    self.statusBar().showMessage("this is not a link")
            else:
                self.statusBar().showMessage("not changed")
        else:
            self.statusBar().showMessage("no text selected")

    def insertLink(self):
        if not self.editor.textCursor().selectedText() == "":
            text = self.editor.textCursor().selectedText()
            dlg = QInputDialog()
            link, ok = dlg.getText(self, 'insert URL', "", QLineEdit.Normal, "", Qt.Dialog)
            if ok:
                if str(link).startswith("http"):
                    self.editor.textCursor().insertHtml("<a href='" + link + "' target='_blank'>" + text + "</a>")
                    self.statusBar().showMessage("link added")
                else:
                    self.statusBar().showMessage("this is no link")
            else:
                self.statusBar().showMessage("no link added")
        else:
            self.statusBar().showMessage("no text selected")


    def convertFromHTML(self):

        old_text = self.editor.textCursor().selectedText()

        self.editor.textCursor().insertHtml(old_text)
        self.statusBar().showMessage("converted to html")


    def convertToHTML(self):

        old_text = QTextDocumentFragment.fromHtml(self.editor.textCursor().selectedText())

        self.editor.textCursor().insertText(old_text.toPlainText())
        self.statusBar().showMessage("converted to plain text")


    def insertImage(self):

        path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath() + "/Pictures/",
                                              "Images (*.png *.PNG *.jpg *.JPG *.bmp *.BMP *.xpm *.gif *.eps)")

        if path:
            # self.editor.append("<img src='" + path + "'/>")

            self.editor.textCursor().insertImage("file://" + path)
            self.statusBar().showMessage("'" + path + "' inserted")

        else:
            self.statusBar().showMessage("no image")


    def grabLine(self):

        text = self.editor.textCursor().block().text()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)


    def about(self):

        link = "<p><a title='Amey Vijeesh' target='_blank'>Amey Vijeesh</a></p>"

        title = "about RichTextEdit"

        message = "<span style='color: #1F9CDD; font-size: 24pt;font-weight: bold;'\
                    >Amey's Word Processor </strong></span></p><br>created by<h3>" + link + "</h3> with hardwork<br>" \
                  + "<br>Created using Python and PyQt5 by Amey" \
                  + "<br>Thank you everyone for encouraging and waiting patiently"

        msg = QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self,
                          Qt.Dialog | Qt.NoDropShadowWindowHint).show()


    def createActions(self):

        for i in range(self.MaxRecentFiles):
            self.recentFileActs.append(
                QAction(self, visible=False,
                        triggered=self.openRecentFile))


    def openRecentFile(self):

        action = self.sender()
        if action:
            if (self.maybeSave()):
                self.openFileOnStart(action.data())

        ### New File


    def newFile(self):

        if self.maybeSave():

            self.editor.clear()
            self.editor.setPlainText(self.mainText)

            self.filename = ""

            self.editor.moveCursor(self.cursor.End)

            self.editor.textCursor().deletePreviousChar()
            self.setWindowTitle("New file- AWP")
            self.setModified(False)


    ### open File
    def openFileOnStart(self, path=None):

        if path:
            inFile = QFile(path)

            if inFile.open(QFile.ReadWrite | QFile.Text):

                data = inFile.readAll()
                codec = QTextCodec.codecForHtml(data)
                unique_string = codec.toUnicode(data)

                if Qt.mightBeRichText(unique_string):

                    self.editor.setHtml(unique_string)

                else:
                    self.editor.setPlainText(unique_string)

                self.filename = path
                self.setModified(False)

                self.filename = QFileInfo(path).fileName()
                self.document = self.editor.document()

                self.setCurrentFile(path)

                self.statusBar().showMessage("loaded file '" + path + "'")

        ### open File


    def openFile(self, path=None):

        if self.maybeSave():

            if not path:

                path, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.homePath() + "/Documents/",
                                                      "RichText Files (*.htm *.html *.xhtml);; Text Files (*.txt *.csv *.py);;All Files (*.*)")
            if path:
                inFile = QFile(path)
                self.openFileOnStart(path)


    def exportPDF(self):

        if self.editor.toPlainText() == "":
            self.statusBar().showMessage("no text")

        else:
            new_name = self.strippedName(self.filename).replace(".html", ".pdf")
            fn, _ = QFileDialog.getSaveFileName(self,
                                                "PDF files (*.pdf);;All Files (*)",
                                                (QDir.homePath() + "/PDF/" + new_name))

            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)

            printer.setOutputFileName(fn)

            self.editor.document().print_(printer)

            ### save


    def fileSave(self):

        if not self.filename:

            return self.fileSaveAs()

        if self.isModified():

            writer = QTextDocumentWriter(self.filename)
            success = writer.write(self.editor.document())

            if success:
                self.editor.document().setModified(False)

                self.setCurrentFile(self.filename)
                self.statusBar().showMessage("saved file '" + self.filename + "'")
            return success

        else:
            self.statusBar().showMessage("already saved")

            ### save


    def fileSave2(self):

        writer = QTextDocumentWriter(self.filename)
        success = writer.write(self.editor.document())

        if success:
            self.editor.document().setModified(False)
            self.setCurrentFile(self.filename)

            self.statusBar().showMessage("saved file '" + self.filename + "'")

    def fileSaveWPS(self, fn):

        writer = QTextDocumentWriter(fn)
        #        writer.setFormat("ODF")
        success = writer.write(self.editor.document())
        if success:
            self.statusBar().showMessage("saved file '" + fn + "'")
        return success


    def fileSaveAs(self):

        if self.editor.toPlainText() == "":

            self.statusBar().showMessage("no text")

        else:
            fn, _ = QFileDialog.getSaveFileName(self, "Save as...", self.filename,
                                                "HTML-Files (*.html *.htm)")

            if fn:
                if not fn.endswith(('.htm', '.html')):
                    fn += '.html'

                self.filename = fn
                return self.fileSave2()


    def fileSaveAsWPS(self):

        if self.editor.toPlainText() == "":

            self.statusBar().showMessage("no text")
        else:
            fn, _ = QFileDialog.getSaveFileName(self, "Save as...",
                                                self.strippedName(self.filename).replace(".html", ""),
                                                "OpenOffice-Files (*.odt)")

            if not fn:
                return False

            lfn = fn.lower()
            if not lfn.endswith(('.odt')):
                fn += '.odt'

            return self.fileSaveWPS(fn)


    def closeEvent(self, e):

        if self.maybeSave():
            e.accept()

        else:
            e.ignore()

        ### ask to save


    def maybeSave(self):

        if not self.isModified():
            return True

        if self.filename.startswith(':/'):
            return True

        ret = QMessageBox.question(self, "Message",
                                   "<h4><p>The document was modified.</p>\n" \
                                   "<p>Do you want to save changes?</p></h4>",
                                   QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Yes:

            if self.filename == "":

                self.fileSaveAs()
                return False

            else:
                self.fileSave()
                return True

        if ret == QMessageBox.Cancel:
            return False

        return True


    def findText(self):

        word = self.findfield.text()

        if self.editor.find(word):
            return
        else:
            self.editor.moveCursor(QTextCursor.Start)

            if self.editor.find(word):
                return


    def handleQuit(self):

        print("Goodbye ...")
        app.quit()


    def document(self):

        return self.editor.document


    def isModified(self):

        return self.editor.document().isModified()


    def setModified(self, modified):

        self.editor.document().setModified(modified)


    def setLineWrapMode(self, mode):

        self.editor.setLineWrapMode(mode)


    def clear(self):

        self.editor.clear()


    def setPlainText(self, *args, **kwargs):

        self.editor.setPlainText(*args, **kwargs)


    def setDocumentTitle(self, *args, **kwargs):

        self.editor.setDocumentTitle(*args, **kwargs)


    def set_number_bar_visible(self, value):

        self.numbers.setVisible(value)


    def replaceAll(self):

        old_text = self.findfield.text()
        new_text = self.replacefield.text()

        if not old_text == "":

            h = self.editor.toHtml().replace(old_text, new_text)
            self.editor.setText(h)

            self.setModified(True)
            self.statusBar().showMessage("all replaced")

        else:
            self.statusBar().showMessage("nothing to replace")


    def replaceOne(self):

        old_text = self.findfield.text()
        new_text = self.replacefield.text()

        if not old_text == "":

            h = self.editor.toHtml().replace(old_text, new_text, 1)
            self.editor.setText(h)
            self.setModified(True)

            self.statusBar().showMessage("one replaced")
        else:
            self.statusBar().showMessage("nothing to replace")


    def setCurrentFile(self, fileName):

        self.filename = fileName

        if self.filename:
            self.setWindowTitle(self.strippedName(self.filename) + "[*]")

        else:
            self.setWindowTitle("no File")

        files = self.settings.value('recentFileList', [])


        try:
            files.remove(fileName)
        except ValueError:
            pass


        files.insert(0, fileName)
        del files[self.MaxRecentFiles:]

        self.settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():

            if isinstance(widget, myEditor):

                widget.updateRecentFileActions()


    def updateRecentFileActions(self):

        the_text = ""
        files = self.settings.value('recentFileList', [])
        numRecentFiles = min(len(files), self.MaxRecentFiles)

        for i in range(numRecentFiles):

            text = "&%d %s" % (i + 1, self.strippedName(files[i]))

            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])

            self.recentFileActs[i].setVisible(True)
            self.recentFileActs[i].setIcon(QIcon.fromTheme("gnome-mime-text-x"))

        for j in range(numRecentFiles, self.MaxRecentFiles):

            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))


    def clearRecentFiles(self, fileName):

        self.settings.clear()
        self.updateRecentFileActions()


    def strippedName(self, fullFileName):

        return QFileInfo(fullFileName).fileName()


    def textBold(self):

        fmt = QTextCharFormat()

        fmt.setFontWeight(self.actionTextBold.isChecked() and QFont.Bold or QFont.Normal)
        self.mergeFormatOnWordOrSelection(fmt)


    def textUnderline(self):

        fmt = QTextCharFormat()

        fmt.setFontUnderline(self.actionTextUnderline.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)


    def textItalic(self):

        fmt = QTextCharFormat()

        fmt.setFontItalic(self.actionTextItalic.isChecked())
        self.mergeFormatOnWordOrSelection(fmt)


    def textFamily(self, family):

        fmt = QTextCharFormat()

        fmt.setFontFamily(family)
        self.mergeFormatOnWordOrSelection(fmt)

    def textSize(self, pointSize):

        pointSize = float(self.comboSize.currentText())

        if pointSize > 0:

            fmt = QTextCharFormat()
            fmt.setFontPointSize(pointSize)

            self.mergeFormatOnWordOrSelection(fmt)


    def textStyle(self, styleIndex):

        cursor = self.editor.textCursor()

        if styleIndex:

            styleDict = {
                1: QTextListFormat.ListDisc,
                2: QTextListFormat.ListCircle,
                3: QTextListFormat.ListSquare,
                4: QTextListFormat.ListDecimal,
                5: QTextListFormat.ListLowerAlpha,
                6: QTextListFormat.ListUpperAlpha,
                7: QTextListFormat.ListLowerRoman,
                8: QTextListFormat.ListUpperRoman,
            }

            style = styleDict.get(styleIndex, QTextListFormat.ListDisc)

            cursor.beginEditBlock()
            blockFmt = cursor.blockFormat()
            listFmt = QTextListFormat()

            if cursor.currentList():
                listFmt = cursor.currentList().format()

            else:
                listFmt.setIndent(1)
                blockFmt.setIndent(0)
                cursor.setBlockFormat(blockFmt)

            listFmt.setStyle(style)
            cursor.createList(listFmt)
            cursor.endEditBlock()

        else:
            block_format = QTextBlockFormat()

            block_format.setObjectIndex(-1)
            cursor.mergeBlockFormat(block_format)


    def textColor(self):

        col = QColorDialog.getColor(self.editor.textColor(), self)

        if not col.isValid():
            return

        fmt = QTextCharFormat()

        fmt.setForeground(col)

        self.mergeFormatOnWordOrSelection(fmt)
        self.colorChanged(col)

    def textAlign(self, action):

        if action == self.actionAlignLeft:
            self.editor.setAlignment(Qt.AlignLeft | Qt.AlignAbsolute)

        elif action == self.actionAlignCenter:
            self.editor.setAlignment(Qt.AlignHCenter)

        elif action == self.actionAlignRight:
            self.editor.setAlignment(Qt.AlignRight | Qt.AlignAbsolute)

        elif action == self.actionAlignJustify:
            self.editor.setAlignment(Qt.AlignJustify)


    def currentCharFormatChanged(self, format):

        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())


    def cursorPositionChanged(self):

        self.alignmentChanged(self.editor.alignment())


    def clipboardDataChanged(self):

        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)


    def mergeFormatOnWordOrSelection(self, format):

        cursor = self.editor.textCursor()

        if not cursor.hasSelection():

            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.editor.mergeCurrentCharFormat(format)


    def fontChanged(self, font):

        self.comboFont.setCurrentIndex(
            self.comboFont.findText(QFontInfo(font).family()
                                    )
        )

        self.comboSize.setCurrentIndex(
            self.comboSize.findText("%s" % font.pointSize()
                                    )
        )

        self.actionTextBold.setChecked(font.bold())

        self.actionTextItalic.setChecked(font.italic())

        self.actionTextUnderline.setChecked(font.underline())


    def colorChanged(self, color):

        pix = QPixmap(26, 20)
        pix.fill(color)

        self.actionTextColor.setIcon(QIcon(pix))


    def alignmentChanged(self, alignment):

        if alignment & Qt.AlignLeft:
            self.actionAlignLeft.setChecked(True)

        elif alignment & Qt.AlignHCenter:
            self.actionAlignCenter.setChecked(True)

        elif alignment & Qt.AlignRight:
            self.actionAlignRight.setChecked(True)

        elif alignment & Qt.AlignJustify:
            self.actionAlignJustify.setChecked(True)


    def handlePrint(self):

        if self.editor.toPlainText() == "":
            self.statusBar().showMessage("no text")

        else:
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QFileDialog.Accepted:

                self.handlePaintRequest(dialog.printer())
                self.statusBar().showMessage("Document printed")


    def handlePrintPreview(self):

        if self.editor.toPlainText() == "":
            self.statusBar().showMessage("no text")

        else:
            dialog = QtPrintSupport.QPrintPreviewDialog()

            dialog.setGeometry(30, 0, self.width() - 60, self.height() - 60)
            dialog.paintRequested.connect(self.handlePaintRequest)

            dialog.exec_()

            self.statusBar().showMessage("Print Preview closed")


    def handlePaintRequest(self, printer):

        printer.setDocName(self.filename)

        document = self.editor.document()
        document.print_(printer)


def myStyleSheet(self):
    return """
QTextEdit
{
background: #fafafa;
color: #202020;
border: 1px solid #1EAE3D;
selection-background-color: #729fcf;
selection-color: #ffffff;
}
QMenuBar
{
background: transparent;
border: 4px;
}
QToolBar
{
background: transparent;
border: 0px;
}
QMainWindow
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
    """


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = myEditor()

    win.setWindowIcon(QIcon.fromTheme("gnome-mime-application-rtf"))

    win.setWindowTitle("Amey's Word Processor" + " (APW)")

    win.setMinimumSize(640, 250)
    win.showMaximized()

    if len(sys.argv) > 1:

        print(sys.argv[1])

        win.openFileOnStart(sys.argv[1])
    app.exec_()

