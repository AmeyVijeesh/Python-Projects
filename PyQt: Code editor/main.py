from PyQt5.QtWidgets import *
from PyQt5.Qsci import *

import sys

from play import *
from extra import *

from os.path import expanduser

import jedi

from PyQt5.QtCore import QRegExp


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget.hide()

        self.ui.actionNew.triggered.connect(self.New)
        self.ui.actionOpen.triggered.connect(self.FileDialog)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionclose.triggered.connect(self.CloseDocument)
        self.ui.actionQuit.triggered.connect(self.quit)

        self.ui.actionFind.triggered.connect(self.find)
        self.ui.actionDeselect.triggered.connect(self.deselect)
        self.ui.actionstatus_bar.triggered.connect(self.ShowStatusbar)

        # used in Finding strings
        self.ui.checkBox.clicked.connect(self.regexp)
        self.ui.checkBox_2.clicked.connect(self.caseSensors)
        self.ui.checkBox_3.clicked.connect(self.CompleteWord)

        # View Menu
        self.ui.actionWordwrap.triggered.connect(self.wordwrap)
        self.ui.actionShow_line_numbers.triggered.connect(self.LineNumber)
        self.ui.actionChange_Font.triggered.connect(self.Font)
        self.ui.actionchange_font_color.triggered.connect(self.FontColor)

        self.ui.actionAbout.triggered.connect(self.about)

        # For highlighting the syntax
        self.ui.actionNormal.triggered.connect(self.normal)
        self.ui.actionBatch.triggered.connect(self.batch)
        self.ui.actionC.triggered.connect(self.cpp)
        self.ui.actionC_2.triggered.connect(self.cpp)
        self.ui.actionC_3.triggered.connect(self.cs)
        self.ui.actionCoffeeScript.triggered.connect(self.cofScript)
        self.ui.actionCSS.triggered.connect(self.css)
        self.ui.actionCmake.triggered.connect(self.cmake)
        self.ui.actionFortan.triggered.connect(self.Fortran)
        self.ui.actionHTML.triggered.connect(self.HTML)
        self.ui.actionJSON.triggered.connect(self.JSON)
        self.ui.actionMakeFIle.triggered.connect(self.makefile)
        self.ui.actionMarkDown.triggered.connect(self.markdown)
        self.ui.actionMat.triggered.connect(self.mat)
        self.ui.actionPascal.triggered.connect(self.Pascal)
        self.ui.actionPerl.triggered.connect(self.Perl)
        self.ui.actionPython.triggered.connect(self.python)
        self.ui.actionRuby.triggered.connect(self.Ruby)
        self.ui.actionSQL.triggered.connect(self.sql)

        self.ui.textEdit.cursorPositionChanged.connect(self.statusbar)

        # toolbar
        self.toolbar()

        # for text editor customization
        self.texteditor()

    def toolbar(self):
        self.ui.toolBar.addAction(self.ui.actionNew)
        self.ui.toolBar.addAction(self.ui.actionOpen)
        self.ui.toolBar.addAction(self.ui.actionclose)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionSave)
        self.ui.toolBar.addAction(self.ui.actionSave_As)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionUndo)
        self.ui.toolBar.addAction(self.ui.actionRedo)

    def texteditor(self):
        self.path = None
        self.ui.textEdit.setIndentationsUseTabs(True)
        self.ui.textEdit.setAutoIndent(True)
        self.ui.textEdit.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.ui.textEdit.setAutoCompletionThreshold(1)
        self.ui.textEdit.setAutoCompletionCaseSensitivity(False)
        self.ui.textEdit.setBraceMatching(1)
        if self.ui.actionWordwrap.isChecked():
            self.ui.textEdit.setWrapMode(QsciScintilla.WrapWord)
        self.label = QLabel()
        self.label_2 = QLabel()
        self.fileConvert = {
            '': 'None',
            'txt': 'None',
            'bat': 'Batch',
            'coffee': 'CoffeeScript',
            'c': 'C++',
            'cpp': 'C++',
            'cxx': 'C++',
            'h': 'C++',
            'hpp': 'C++',
            'hxx': 'C++',
            'cs': 'C#',
            'css': 'CSS',
            'd': 'D',
            'f': 'Fortran',
            'html': 'HTML',
            'java': 'Java',
            'js': 'JavaScript',
            'json': 'JSON',
            'md': 'Markdown',
            'mlx': 'Matlab',
            'pas': 'Pascal',
            'pl': 'Perl',
            'py': 'Python',
            'rb': 'Ruby',
            'sql': 'SQL',
            'xml': 'XML'
        }

    def ShowStatusbar(self):
        if self.ui.actionstatus_bar.isChecked():
            self.ui.statusBar.show()
        else:
            self.ui.statusBar.hide()

    def statusbar(self):
        textedit = self.ui.textEdit
        messenger = textedit.SendScintilla
        pos = messenger(textedit.SCI_GETCURRENTPOS)
        column_number = messenger(textedit.SCI_GETCOLUMN, pos)
        line_numbers = messenger(textedit.SCI_LINEFROMPOSITION, pos)
        self.label.setText("line " + str(line_numbers + 1) + ", column " + str(column_number + 1))
        self.ui.statusBar.addWidget(self.label, 5)
        self.ui.statusBar.addWidget(self.label_2)
        self.showFileType()

    def showFileType(self):
        if self.path == None:
            self.label_2.setText("Normal")
        else:
            if '.' in self.path:
                extension = self.path.split('.')[-1]
            else:
                extension = ''
            if extension in self.fileConvert:
                language = self.fileConvert.get(extension)
                self.label_2.setText(language)
            else:
                self.label_2.setText("Normal")

    def New(self):
        self.new = MainWindow()
        self.new.show()

    def FileDialog(self):
        home = expanduser('~')
        path = QFileDialog.getOpenFileName(self, "Open File", home)[0]
        if path:
            self.openfile = open(path, 'r')
            text = self.openfile.read()
            self.ui.textEdit.setText(str(text))
            if '.' in path:
                extension = path.split('.')[-1]
            else:
                extension = ''
            self.path = path
            if extension in self.fileConvert:
                language = self.fileConvert.get(extension)
                self.SyntaxHighlight(language)
            else:
                self.SyntaxHighlight('None')
            self.showFileType()

    def save(self):
        if self.path is None:
            return self.saveAs()
        if self.path:
            text = self.ui.textEdit.app()
            savefile = open(self.path, 'w')
            savefile.write(str(text))
            if '.' in self.path:
                extension = self.path.split('.')[-1]
            else:
                extension = ''
            if extension in self.fileConvert:
                language = self.fileConvert.get(extension)
                self.SyntaxHighlight(language)
            else:
                self.SyntaxHighlight('None')
            self.showFileType()

    def saveAs(self):
        home = expanduser('~')
        path = QFileDialog().getSaveFileName(self, "Save File", home)[0]
        if path:
            savefile = open(path, 'w')
            text = self.ui.textEdit.app()
            savefile.write(str(text))
            self.path = path
            if '.' in path:
                extension = path.split('.')[-1]
            else:
                extension = ''
            if extension in self.fileConvert:
                language = self.fileConvert.get(extension)
                self.SyntaxHighlight(language)
            else:
                self.SyntaxHighlight('None')
            self.showFileType()

    def SyntaxHighlight(self, lexer):
        # Converting the language to lexer
        self.languageToLexer = {
            'None': None,
            'Batch': QsciLexerBatch,
            'CMake': QsciLexerCMake,
            'CoffeeScript': QsciLexerCoffeeScript,
            'C++': QsciLexerCPP,
            'C#': QsciLexerCSharp,
            'CSS': QsciLexerCSS,
            'Fortran': QsciLexerFortran,
            'HTML': QsciLexerHTML,
            'Java': QsciLexerJava,
            'JavaScript': QsciLexerJavaScript,
            'JSON': QsciLexerJSON,
            'Makefile': QsciLexerMakefile,
            'Markdown': QsciLexerMarkdown,
            'Matlab': QsciLexerMatlab,
            'Pascal': QsciLexerPascal,
            'Perl': QsciLexerPerl,
            'Python': QsciLexerPython,
            'Ruby': QsciLexerRuby,
            'SQL': QsciLexerSQL,
            'XML': QsciLexerXML
        }

        lang = self.languageToLexer.get(lexer)
        if lang == None:
            pass
        else:
            self.lexer = lang(self)
            self.ui.textEdit.setLexer(self.lexer)
            if lexer == "Python":
                self.autocomplete()

    def autocomplete(self):
        self.api = QsciAPIs(self.lexer)

        source = self.ui.textEdit.app()
        line = 1
        column = 0
        path = ""
        script = jedi.Script(source, line, column, path)
        complete = script.completions()
        l = []

        for i in complete:
            l.append(i.name)
        for i in l:
            self.api.add(i)
        self.api.prepare()

    def CloseDocument(self):
        text = self.ui.textEdit.app()
        if text == "":
            text = ""
            self.ui.textEdit.setText(text)
        else:
            if self.path is None:
                a = QMessageBox.question(self, "Save Before Closing", "Do you want to save the document?", QMessageBox(
                ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                if a == QMessageBox().Yes:
                    self.saveAs()
                    text = ""
                    self.ui.textEdit.setText(text)
                elif a == QMessageBox().No:
                    text = ""
                    self.ui.textEdit.setText(text)
                elif a == QMessageBox().Cancel:
                    pass

            else:
                f = open(self.path, 'r')
                file_text = f.read()
                if file_text == text:
                    text = ""
                    self.ui.textEdit.setText(text)
                else:
                    a = QMessageBox().question(self, "Save Before Closing", "Do you want to save the document?",
                                               QMessageBox().Yes | QMessageBox().No | QMessageBox().Cancel,
                                               QMessageBox().Cancel)
                    if a == QMessageBox().Yes:
                        self.save()
                        text = ""
                        self.ui.textEdit.setText(text)
                    elif a == QMessageBox().No:
                        text = ""
                        self.ui.textEdit.setText(text)
                    elif a == QMessageBox().Cancel:
                        pass
        self.path = None
        self.showFileType()

    def quit(self):
        text = self.ui.textEdit.app()
        if text == "":
            a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                       QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
            if a == QMessageBox().Yes:
                sys.exit()
            else:
                pass
        else:
            if self.path is None:
                a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit", QMessageBox(
                ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                if a == QMessageBox().Yes:
                    self.saveAs()
                    sys.exit()
                elif a == QMessageBox().No:
                    sys.exit()
                else:
                    pass
            else:
                f = open(self.path, 'r')
                filetext = f.read()
                if filetext == text:
                    a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                               QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
                    if a == QMessageBox().Yes:
                        sys.exit()
                else:
                    a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit",
                                             QMessageBox(
                                             ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                    if a == QMessageBox().Yes:
                        self.save()
                        sys.exit()
                    elif a == QMessageBox().No:
                        sys.exit()
                    else:
                        pass

    def find(self):
        self.ui.widget.show()

        self.re = False
        self.cs = False
        self.wo = False

        self.ui.pushButton.clicked.connect(self.hidefindbar)
        self.ui.pushButton_2.clicked.connect(self.search)
        self.ui.pushButton_3.clicked.connect(self.replace)

    def hidefindbar(self):  # closes the find widget
        self.ui.widget.hide()

    def search(self):  # for finding the strings
        textEdit = self.ui.textEdit
        search_text = self.ui.lineEdit.app()
        self.ui.textEdit.findFirst(search_text, self.re, self.cs, self.wo, False)

    # used in finding strings

    def regexp(self):
        if self.ui.checkBox.isChecked():
            self.re = True
        else:
            self.re = False

    def caseSensors(self):
        if self.ui.checkBox_2.isChecked():
            self.cs = True
        else:
            self.cs = False

    def CompleteWord(self):
        if self.ui.checkBox_3.isChecked():
            self.wo = True
        else:
            self.wo = False

    def replace(self):
        replace_text = self.ui.lineEdit_2.app()
        textedit = self.ui.textEdit
        textedit.replace(replace_text)

    def deselect(self):
        textedit = self.ui.textEdit
        messenger = self.ui.textEdit.SendScintilla
        pos = messenger(textedit.SCI_GETCURRENTPOS)
        messenger(textedit.SCI_SETEMPTYSELECTION, pos)

    def wordwrap(self):
        if self.ui.actionWordwrap.isChecked():
            self.ui.textEdit.setWrapMode(QsciScintilla.WrapWord)
        else:
            self.ui.textEdit.setWrapMode(QsciScintilla.WrapNone)

    def LineNumber(self):  # Set the Line Numbers
        if self.ui.actionShow_line_numbers.isChecked():
            self.ui.textEdit.setMarginType(1, QsciScintilla.NumberMargin)
            self.ui.textEdit.setMarginWidth(1, "0000")
        else:
            self.ui.textEdit.setMarginWidth(1, "")

    def Font(self):
        font_dialog, i = QFontDialog().getFont()
        if i:
            self.ui.textEdit.setFont(font_dialog)

    def FontColor(self):
        color = QColorDialog().getColor()
        if color.isValid:
            self.ui.textEdit.setColor(color)

    def about(self):
        AboutDialog().exec_()


    def normal(self):
        language = None
        self.SyntaxHighlight(language)

    def batch(self):
        language = "Batch"
        self.SyntaxHighlight(language)

    def cpp(self):
        language = "C++"
        self.SyntaxHighlight(language)

    def cs(self):
        language = "C#"
        self.SyntaxHighlight(language)

    def cofScript(self):
        language = "CoffeeScript"
        self.SyntaxHighlight(language)

    def css(self):
        language = "CSS"
        self.SyntaxHighlight(language)

    def cmake(self):
        language = "CMake"
        self.SyntaxHighlight(language)

    def Fortran(self):
        language = "Fortran"
        self.SyntaxHighlight(language)

    def HTML(self):
        language = "HTML"
        self.SyntaxHighlight(language)

    def JSON(self):
        language = "JSOn"
        self.SyntaxHighlight(language)

    def makefile(self):
        language = "Makefile"
        self.SyntaxHighlight(language)

    def markdown(self):
        language = "Markdown"
        self.SyntaxHighlight(language)

    def mat(self):
        language = "Matlab"
        self.SyntaxHighlight(language)

    def Pascal(self):
        language = "Pascal"
        self.SyntaxHighlight(language)

    def Perl(self):
        language = "Perl"
        self.SyntaxHighlight(language)

    def python(self):
        language = "Python"
        self.SyntaxHighlight(language)

    def Ruby(self):
        language = "Ruby"
        self.SyntaxHighlight(language)

    def sql(self):
        language = "SQL"
        self.SyntaxHighlight(language)

    def XML(self):
        language = "XML"
        self.SyntaxHighlight(language)

    def closeEvent(self, events):
        text = self.ui.textEdit.app()
        if text == "":
            a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                       QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
            if a == QMessageBox().Yes:
                events.accept()
            else:
                events.ignore()
        else:
            if self.path is None:
                a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit", QMessageBox(
                ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                if a == QMessageBox().Yes:
                    self.saveAs()
                    events.accept()
                elif a == QMessageBox().No:
                    events.accept()
                else:
                    events.ignore()
            else:
                f = open(self.path, 'r')
                file_text = f.read()
                if file_text == text:
                    a = QMessageBox().question(self, "Exit Dialog", "Do you want to exit",
                                               QMessageBox().Yes | QMessageBox().No, QMessageBox().No)
                    if a == QMessageBox().Yes:
                        events.accept()
                    else:
                        events.ignore()
                else:
                    a = QMessageBox.question(self, "Save Before Closing", "Do you want to save Before exit",
                                             QMessageBox(
                                             ).Yes | QMessageBox().No | QMessageBox().Cancel, QMessageBox().Cancel)
                    if a == QMessageBox().Yes:
                        self.save()
                        events.accept()
                    elif a == QMessageBox().No:
                        events.accept()
                    else:
                        events.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
