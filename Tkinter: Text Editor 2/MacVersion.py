from tkinter import *
from tkinter.ttk import Notebook, Combobox
from tkinter import font
from tkinter import colorchooser
import tkinter.messagebox as messagebox
from datetime import datetime
import time
import webbrowser
import pyttsx3


class UiComponents(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

        self.text = Text(self, bg='white', foreground="black", undo=True, font=('Calibri', 12),
                         insertbackground='black', height=35, width=135,
                         selectbackground="blue")

        self.scrollbar = Scrollbar(self, orient=VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)

        def find_replace(event=None):
            def find_text():
                chars = char_entry.get()
                self.text.tag_remove('found', '1.0', END)

                if chars:
                    idx = '1.0'

                    while 1:
                        idx = self.text.search(chars, idx, nocase=1, stopindex=END)

                        if not idx:
                            break

                        last_idx = '% s+% dc' % (idx, len(chars))

                        self.text.tag_add('found', idx, last_idx)
                        idx = last_idx

                    self.text.tag_config('found', background='#5ED600')

            def rep_text():
                chars = char_entry.get()
                rep_chars = replace_word.get()
                self.text.tag_remove('found', '1.0', END)

                if chars and rep_chars:
                    idx = '1.0'

                    while 1:
                        idx = self.text.search(chars, idx, nocase=1, stopindex=END)

                        if not idx:
                            break

                        last_idx1 = '% s+% dc' % (idx, len(chars))
                        self.text.tag_add('found', idx, last_idx1)

                        last_idx = '% s+% dc' % (idx, len(rep_chars))
                        self.text.delete(idx, last_idx1)
                        self.text.insert(idx, rep_chars)

                        self.text.tag_add('found', idx, last_idx)
                        idx = last_idx
                    self.text.tag_config('found', background='yellow')

            def highlight():
                self.text.tag_remove('found', '1.0', END)

            find_top_level = Toplevel()
            find_top_level.title("Find or replace text")
            find_top_level.geometry("450x200")
            find_top_level.config(bg='white')
            find_top_level.resizable(False, False)

            font1 = 'Calibri', 12

            find_label = Label(find_top_level, text="Find: ", bg='white', font=font1)
            find_label.place(x=35, y=25)

            char_entry = Entry(find_top_level, bg='white', font=font1, highlightbackground='black',
                               highlightthickness=4)
            char_entry.place(x=225, y=25)

            find_btn1 = Button(find_top_level, text="Find", command=find_text, width=7,
                               relief='ridge')
            find_btn1.place(x=175, y=75)

            replace_label = Label(find_top_level, text="Replace: ", bg='white', font=font1)
            replace_label.place(x=35, y=115)

            replace_word = Entry(find_top_level, bg='white', font=font1, highlightbackground='black',
                                 highlightthickness=4)
            replace_word.place(x=225, y=115)

            replace_btn = Button(find_top_level, text="Replace", command=rep_text, width=7,
                                 relief='ridge')
            replace_btn.place(x=175, y=160)

            highlight_btn = Checkbutton(find_top_level, text="Remove highlights", bg='white', command=highlight,
                                        width=20)
            highlight_btn.place(x=300, y=170)

        def refactor():
            search_top_level = Toplevel(root)
            search_top_level.title('Refactor')
            search_top_level.resizable(False, False)
            search_top_level.config(bg='white')

        def find(event=None):
            search_top_level = Toplevel(root)
            search_top_level.title('Find Text')
            search_top_level.resizable(False, False)
            search_top_level.config(bg='white')

            Label(search_top_level, text="Find:", bg='white').grid(row=0, column=0, sticky='e')

            search_entry_widget = Entry(search_top_level, width=25)
            search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
            search_entry_widget.focus_set()

            ignore_case_value = IntVar()
            Checkbutton(search_top_level, text='Ignore Case', bg='white', variable=ignore_case_value).grid(row=1,
                                                                                                           column=1,
                                                                                                           sticky='e',
                                                                                                           padx=2,
                                                                                                           pady=2)
            Button(search_top_level, text="Find", underline=0, relief='solid', bg='white',
                   command=lambda: search_output(
                       search_entry_widget.get(), ignore_case_value.get(),
                       self.text, search_top_level, search_entry_widget)
                   ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

        def search_output(needle, if_ignore_case, content_text, search_top_level, search_box):
            content_text.tag_remove('match', '1.0', END)
            matches_found = 0

            if needle:
                start_pos = '1.0'

                while True:
                    start_pos = content_text.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)

                    if not start_pos:
                        break

                    end_pos = '{} + {}c'.format(start_pos, len(needle))
                    content_text.tag_add('match', start_pos, end_pos)
                    matches_found += 1
                    start_pos = end_pos
                content_text.tag_config('match', background='yellow', foreground='blue')

            search_box.focus_set()
            matches_found_text = '{} matches found'.format(matches_found)
            search_top_level.title(matches_found_text)

        def change_font(event=None):
            try:
                font_change = font.Font(self.text, self.text.cget("font"))
                font_change.configure(family=font_family.get())

                if len(self.font_tag_name) == 0:
                    temp_store = [self.font_tag_count, self.text.index("sel.first"),
                                  self.text.index("sel.last")]
                    self.font_tag_name.append(temp_store)
                    temp = self.font_tag_name[0][0]
                    self.font_tag_count += 1
                else:
                    def search():
                        start_point = self.text.index("sel.first")
                        end = self.text.index("sel.last")
                        for take in self.font_tag_name:
                            if take[1] == start_point and take[2] == end:
                                temp1 = take[0]
                                return temp1
                        return -1

                    temp = search()

                    if temp == -1:
                        temp_store = [self.font_tag_count, self.text.index("sel.first"),
                                      self.text.index("sel.last")]
                        self.font_tag_name.append(temp_store)
                        temp = self.font_tag_name[self.font_tag_count][0]
                        self.font_tag_count += 1

                self.text.tag_configure(temp, font=font_change)
                self.text.tag_add(temp, "sel.first", "sel.last")

            except TclError:
                try:
                    self.text.configure(font=(font_family.get(), font_size.get()))

                except TclError:
                    self.text.configure(font=(font_family.get(), 12))

        def update_char_length(event=None):
            string_in_text = self.text.get('1.0', 'end-1c')
            string_length = len(string_in_text)
            chars_label['text'] = f'Total Characters: {string_length}'

        def count_lines(event):
            (line, chars) = map(int, event.widget.index("end-1c").split("."))
            words = len(text.get("1.0", "end-1c").split())

            lines_label['text'] = f'Total Lines: {line}'
            words_label['text'] = f'Total Words: {words}'

        self.font_tag_name = []
        self.font_tag_count = 0

        def change_background():
            selected_color = colorchooser.askcolor()
            self.text['bg'] = selected_color[1]

        def align_left():
            try:
                start_pos = list(self.text.index(INSERT))
                empty_space = list(
                    self.text.get(int(start_pos[0]) * 1.0, "sel.first"))

                if len(empty_space) == 0 or empty_space[0] == '\t' or \
                        empty_space[0] == ' ':
                    get_all_text = self.text.get("sel.first", "sel.last")
                    self.text.tag_configure("left", justify=LEFT)
                    self.text.delete("sel.first", "sel.last")
                    self.text.insert(int(start_pos[0]) * 1.0, get_all_text, "left")
                else:
                    messagebox.showerror("", "Text already aligned.")
            except TclError:
                messagebox.showerror("", "Select text to change the alignment.")

        def align_center():
            try:
                store = list(self.text.index("sel.first"))
                store = int(store[0]) * 1.0
                checking_if_empty_space_present = list(self.text.get("sel.last", "current lineend"))

                if len(checking_if_empty_space_present) == 0 or checking_if_empty_space_present[
                    len(checking_if_empty_space_present) - 1] == '\t' or checking_if_empty_space_present[
                    len(checking_if_empty_space_present) - 1] == ' ':
                    get_all_text = self.text.get(store, "sel.last")
                    self.text.tag_configure("middle", justify=CENTER)
                    self.text.delete(store, "sel.last")
                    self.text.insert(INSERT, get_all_text, "middle")
                else:
                    messagebox.showerror("", "Right side is occupied")
            except TclError:
                messagebox.showerror("", "Nothing selected here")

        def align_right():
            try:
                store = list(self.text.index("sel.first"))
                store = int(store[0]) * 1.0
                checking_if_empty_space_present = list(self.text.get("sel.last", "current lineend"))

                if len(checking_if_empty_space_present) == 0 or checking_if_empty_space_present[
                    len(checking_if_empty_space_present) - 1] == '\t' or checking_if_empty_space_present[
                    len(checking_if_empty_space_present) - 1] == ' ':
                    get_all_text = self.text.get(store, "sel.last")
                    self.text.tag_configure("right", justify=RIGHT)
                    self.text.delete(store, "sel.last")
                    self.text.insert(INSERT, get_all_text, "right")
                else:
                    messagebox.showerror("", "Text already aligned")
            except TclError:
                messagebox.showerror("", "Select text to change the alignment.")

        def bold(event=None):
            try:
                get_font = font.Font(self.text, self.text.cget("font"))
                get_font.configure(weight="bold")

                self.text.tag_configure("make_bold", font=get_font)

                current_tags = self.text.tag_names("sel.first")

                if "make_bold" in current_tags:
                    self.text.tag_remove("make_bold", "sel.first", "sel.last")
                else:
                    self.text.tag_add("make_bold", "sel.first", "sel.last")
            except TclError:

                try:
                    self.text.config(font=(font_family.get(), font_size.get(), 'bold'))

                except TclError:
                    self.text.config(font=(font_family.get(), 12, 'bold'))

        def italic(e=None):
            try:
                get_font = font.Font(self.text, self.text.cget("font"))
                get_font.configure(slant="italic")

                self.text.tag_configure("make_italic", font=get_font)

                current_tags = self.text.tag_names("sel.first")

                if "make_italic" in current_tags:
                    self.text.tag_remove("make_italic", "sel.first", "sel.last")
                else:
                    self.text.tag_add("make_italic", "sel.first", "sel.last")
            except TclError:

                try:
                    self.text.config(font=(font_family.get(), font_size.get(), 'italic'))

                except TclError:
                    self.text.config(font=(font_family.get(), 12, 'italic'))


        def underline(e=None):
            try:
                get_font = font.Font(self.text, self.text.cget("font"))
                get_font.configure(underline=True)

                self.text.tag_configure("make_underline", font=get_font)

                current_tags = self.text.tag_names("sel.first")

                if "make_underline" in current_tags:
                    self.text.tag_remove("make_underline", "sel.first", "sel.last")
                else:
                    self.text.tag_add("make_underline", "sel.first", "sel.last")
            except TclError:
                try:
                    self.text.config(font=(font_family.get(), font_size.get(), 'underline'))

                except TclError:
                    self.text.config(font=(font_family.get(), 12, 'underline'))

        def speak():
            engine = pyttsx3.init()
            content = self.text.get("1.0", END)

            if len(content) >= 200:
                messagebox.showerror("Limit reached",
                                     "At a time, you can only use the speak feature for up to 200 characters. "
                                     "Please make sure that the characters of your file is less than 200")

            else:
                engine.say(content)
                engine.runAndWait()

        def dark_mode():
            root['bg'] = '#2A2A2A'
            toolbar['bg'] = '#2A2A2A'
            self.text['bg'] = '#2A2A2A'
            self.text['fg'] = '#FFFFFF'
            self.text['insertbackground'] = '#FFFFFF'

        def light_mode():
            root['bg'] = '#FFFFFF'
            toolbar['bg'] = '#FFFFFF'
            self.text['bg'] = '#FFFFFF'
            self.text['fg'] = '#2A2A2A'
            self.text['insertbackground'] = '#2A2A2A'

        def search_wikipedia():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = "_".join(get_text.split(" "))
                webbrowser.open(f'https://en.wikipedia.org/wiki/{get_text}')

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to search Wikipedia')

        def search_google():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = '_'.join(get_text.split(" "))
                webbrowser.open(f"https://google.com/search?q={get_text}")

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to search Google')

        def search_bing():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = '_'.join(get_text.split(" "))
                webbrowser.open(f"https://bing.com/search?q={get_text}")

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to search Bing')

        def search_amazon():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = '_'.join(get_text.split(' '))
                webbrowser.open(f"https://www.amazon.com/s?k={get_text}")

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to search Amazon')

        def google_translate():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = '%20'.join(get_text.split(' '))
                webbrowser.open(f"https://translate.google.com/?sl=auto&tl=en&text={get_text}&op=translate")

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to translate via Google translate')

        def bing_translate():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = '%20'.join(get_text.split(' '))
                webbrowser.open(f"https://www.bing.com/translator/?ref=TThis&text={get_text}&from=auto&to=eng")

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to translate it via Bing Translator')

        def google_maps():
            try:
                get_text = self.text.get("sel.first", "sel.last")
                get_text = '+'.join(get_text.split(' '))
                webbrowser.open(f"https://www.google.com/maps/place/{get_text}")

            except TclError:
                messagebox.showerror("No selection",
                                     'Currently you have not selected text in your document. '
                                     'Please select text to map it via Google Maps')

        def undo():

            try:
                self.text.edit_undo()

            except TclError:
                messagebox.showerror(
                    "Nothing to Undo",
                    "You have not typed anything to undo. Please type and try again!"
                )

        def redo():

            try:
                self.text.edit_redo()

            except TclError:
                messagebox.showerror(
                    "Nothing to Redo",
                    "You have not done an undo to redo. Please do and undo and try again!"
                )

        def add_date():
            current_date = datetime.today().strftime("%A, %d.%b.%y")
            text.insert("1.0", chars=f'{current_date}\n')

        def change_select_bg():
            selected_color = colorchooser.askcolor()
            self.text.config(selectbackground=selected_color[1])

        def change_select_fg():
            selected_color = colorchooser.askcolor()
            self.text.config(selectforeground=selected_color[1])

        def change_insert_bg():
            selected_color = colorchooser.askcolor()
            self.text.config(insertbackground=selected_color[1])

        def convert_upper():
            content = self.text.get("1.0", END)
            self.text.delete("1.0", END)

            upper_content = content.upper()
            self.text.insert("1.0", upper_content)

        def convert_lower():
            content = self.text.get("1.0", END)
            self.text.delete("1.0", END)

            lower_content = content.lower()
            self.text.insert("1.0", lower_content)

        def add_time():
            current_time = time.strftime("%H:%M Uhr ")
            text.insert("1.0", chars=f'{current_time}\n')

        def insert_date_time():
            add_time()
            add_date()

        def select_all():
            self.text.event_generate("<<SelectAll>>")

        def cut():
            self.text.event_generate("<<Cut>>")

        def copy():
            self.text.event_generate("<<Copy>>")

        def paste():
            self.text.event_generate("<<Paste>>")

        def clear(event=None):
            self.text.delete("1.0", END)

        undo_button = Button(self, text='Undo', relief='ridge', command=undo,
                             width=6)
        undo_button.place(x=30, y=10)

        redo_button = Button(self, text='Redo', relief='ridge', command=redo,
                             width=6)
        redo_button.place(x=100, y=10)

        copy_button = Button(toolbar, text='Copy', command=copy, relief='ridge',
                             width=6)
        copy_button.place(x=785, y=5)

        cut_button = Button(toolbar, text='Cut', command=cut, relief='ridge',
                            width=6)
        cut_button.place(x=720, y=5)

        paste_button = Button(toolbar, text='Paste', command=paste, relief='ridge',
                              width=6)
        paste_button.place(x=845, y=5)

        select_button = Button(self, text='Select All', command=select_all, relief='ridge',
                               width=7)
        select_button.place(x=170, y=10)

        clear_btn = Button(self, text='Clear', relief='ridge', command=clear,
                           width=6)
        clear_btn.place(x=250, y=10)

        bg_btn = Button(toolbar, text='Background', command=change_background)
        bg_btn.place(x=920, y=5)

        Label(self, text="", relief=FLAT, height=2, bg='white', font='Arial-black').pack()

        lines_label = Label(self, text='Total lines: 0', fg='black', font=('Calibri', 12), relief='ridge', width=15,
                            bg='white')
        lines_label.place(x=320, y=10)

        chars_label = Label(self, text='Total Characters: 0', fg='black', font=('Calibri', 12), relief='ridge',
                            width=20,
                            bg='white')
        chars_label.place(x=450, y=10)

        words_label = Label(self, text='Total Words: 0', fg='black', font=('Calibri', 12), relief='ridge', width=15,
                            bg='white')
        words_label.place(x=620, y=10)

        find_btn = Button(root, text='Find and Replace', relief='ridge', command=find_replace)
        find_btn.place(x=600, y=5)

        size_var = IntVar()
        size = tuple(range(10, 90))
        font_size = Combobox(self, width=10, textvariable=size_var, state='readonly')
        font_size['values'] = size
        font_size.current(size.index(12))
        font_size.place(x=1000, y=12)

        fonts = font.families()
        font_family = StringVar()
        font_box = Combobox(self, width=20, textvariable=font_family, state='readonly')
        font_box['values'] = fonts
        font_box.current(fonts.index("Arial"))
        font_box.place(x=760, y=12)

        self.numberLines = TextLineNumbers(self, width=40, bg='#2A2A2A')
        self.numberLines.attach(self.text)

        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.numberLines.pack(side=LEFT, fill=Y, padx=(5, 0))
        self.text.pack(fill='both', expand=1, padx=0, pady=4)

        self.text.bind('<KeyPress>', update_char_length)
        self.text.bind('<KeyRelease>', update_char_length)

        self.text.bind("<Key>", self.onPressDelay)
        self.text.bind("<Button-1>", self.numberLines.redraw)
        self.scrollbar.bind("<Button-1>", self.onScrollPress)
        self.text.bind("<MouseWheel>", self.onPressDelay)

        bindtags = list(self.text.bindtags())
        bindtags.insert(2, "custom")
        self.text.bindtags(tuple(bindtags))
        self.text.bind_class("custom", "<Key>", count_lines)

        font_box.bind("<<ComboboxSelected>>", change_font)
        font_size.bind("<<ComboboxSelected>>", change_font)

        def scr_menu():
            menu = Menu(root)
            root.config(menu=menu)

            file = Menu(menu, tearoff=False)
            menu.add_cascade(label='File', menu=file)

            edit = Menu(menu, tearoff=False)
            menu.add_cascade(label='Edit', menu=edit)

            edit.add_command(label=" Cut ", command=cut)

            edit.add_command(label=" Copy ", command=copy)

            edit.add_command(label=" Paste ", command=paste)

            edit.add_separator(background='black')

            edit.add_command(label=" Undo ", command=undo)

            edit.add_command(label=" Redo ", command=redo)

            edit.add_command(label=" Select all ", command=select_all)

            edit.add_separator(background='black')

            edit.add_command(label=" Find ", command=find)

            edit.add_command(label=" Clear ", command=clear)

            edit.add_command(label=' Find and Replace ', command=find_replace)

            edit.add_separator()

            edit.add_command(label=" Convert to Upper case ",  command=convert_upper)

            edit.add_command(label=" Convert to Lower case ", command=convert_lower)

            edit.add_separator()

            edit.add_command(label=" Bold ", command=bold)
            edit.add_command(label=" Italic  ", command=italic)
            edit.add_command(label=" Underline ", command=underline)

            view = Menu(menu, tearoff=False)
            menu.add_cascade(label='View', menu=view)
            view.add_command(label=' Dark Mode ', command=dark_mode)
            view.add_command(label=' Light mode ', command=light_mode)

            insert = Menu(menu, tearoff=False)
            menu.add_cascade(label='Insert', menu=insert)

            insert.add_command(label=" Insert date ", command=add_date)

            insert.add_command(label=" Insert Time ", command=select_all)

            insert.add_command(label=' Insert Date and Time ', command=insert_date_time)

            text_menu = Menu(menu, tearoff=False)
            menu.add_cascade(label='Text Edit', menu=text_menu)

            text_menu.add_command(label=' Bold ', command=bold)

            text_menu.add_command(label=' Italic ', command=italic)

            text_menu.add_command(label=' Underline ', command=underline)

            text_menu.add_command(label=' Align Left', command=align_left)

            text_menu.add_command(label=' Align Center', command=align_center)

            text_menu.add_command(label=' Align Right', command=align_right)

            search_menu = Menu(menu, tearoff=False)
            menu.add_cascade(label='Search', menu=search_menu)

            search_menu.add_command(label=' Google ', command=search_google)

            search_menu.add_command(label=' Bing ', command=search_bing)

            search_menu.add_separator()

            search_menu.add_command(label=' Wikipedia ', command=search_wikipedia)

            search_menu.add_command(label=' Amazon ', command=search_amazon)

            search_menu.add_separator(background='black')

            search_menu.add_command(label=' Google Translate ', command=google_translate)

            search_menu.add_command(label=' Bing Translator ', command=bing_translate)

            search_menu.add_separator(background='black')

            search_menu.add_command(label=' Map it using Google maps ', command=google_maps)

            search_menu.add_command(label=' Map it using Bing maps ', command=bing_translate)

            custom_menu = Menu(menu, tearoff=False)
            menu.add_cascade(label='Customisation', menu=custom_menu)

            custom_menu.add_command(label=' Change selection background ', command=change_select_bg)
            custom_menu.add_command(label=' Change selection foreground ', command=change_select_fg)
            custom_menu.add_command(label=' Change insert background ', command=change_insert_bg)

            tools = Menu(menu, tearoff=False)
            menu.add_cascade(label='Tools', menu=tools)

            tools.add_command(label=' Find and Replace ', command=find_replace)

            tools.add_separator(background='black')
            tools.add_command(label=' Stop calculating Working time ', command=stop)

            tools.add_separator(background='black')
            tools.add_command(label=' Speak ', command=speak)

            help_menu = Menu(menu, tearoff=False)
            menu.add_cascade(label='Help', menu=help_menu)

            root.bind("<Control-Key-f>", find_replace)
            root.bind("<Alt-Key-x>", clear)
            root.bind("<Control-Key-b>", bold)
            root.bind("<Control-Key-i>", italic)
            root.bind("<Alt-Key-u>", underline)

        scr_menu()

    def onScrollPress(self, *args):
        self.scrollbar.bind("<B1-Motion>", self.numberLines.redraw)

    def onScrollRelease(self, *args):
        self.scrollbar.unbind("<B1-Motion>", self.numberLines.redraw)

    def onPressDelay(self, *args):
        self.after(2, self.numberLines.redraw)

    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)

    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.text.index(*args, **kwargs)

    def redraw(self):
        self.numberLines.redraw()


class TextLineNumbers(Canvas):
    Canvas.text_widget = None

    def attach(self, text_widget):
        self.text_widget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.text_widget.index("@0,0")
        while True:
            d_line = self.text_widget.dlineinfo(i)
            if d_line is None:
                break
            y = d_line[1]
            line_numbers = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=line_numbers, fill="white")
            i = self.text_widget.index("%s+1line" % i)


counter = 66600
running = False


def count_time(event=None):
    def count():
        if running:
            global counter

            if counter == 66600:
                display = "Working time: 00:00:00"

            else:
                tt = datetime.fromtimestamp(counter)
                string = tt.strftime("Working time: " + "%H:%M:%S")
                display = string

            time_label['text'] = display
            time_label.after(1000, count)
            counter += 1

    count()


def start(event=None):
    global running
    running = True
    count_time(time_label)
    start_btn['state'] = 'disabled'
    stop_btn['state'] = 'normal'


def stop():
    global running
    start_btn['state'] = 'normal'
    stop_btn['state'] = 'disabled'
    running = False


root = Tk()
root.config(bg='white')
root.geometry("1260x670")

toolbar = Frame(root, bg='white', height=45)
toolbar.pack(expand=False, fill='x')

tab = Frame(root)
tab.pack()

text = UiComponents(tab, bg='white')
text.pack()

time_label = Label(root, text='Working time: 00:00:00', fg='black', font=('Calibri', 12), relief='ridge', width=20,
                   bg='white')
time_label.place(x=200, y=5)

stop_btn = Button(root, text='Stop Counting', relief='ridge', command=stop)
stop_btn.place(x=380, y=5)

start_btn = Button(root, text='Resume Counting', relief='ridge', state='disabled',
                   command=start)
start_btn.place(x=480, y=5)

start(time_label)
root.after(200, text.redraw())

# mainloop
root.mainloop()
