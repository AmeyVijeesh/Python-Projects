# AText Editor made using Tkinter

from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter.filedialog import *
from tkinter import colorchooser, font
from tkinter.scrolledtext import ScrolledText
from datetime import datetime, date
import time
import os


# Buttons: #0084BA

def hover(widget, entrance_fg, exit_fg, on_entrance, on_exit):
    widget.bind("<Enter>", func=lambda e: widget.config(
        bg=on_entrance,
        fg=entrance_fg
    ))

    widget.bind("<Leave>", func=lambda e: widget.config(
        bg=on_exit,
        fg=exit_fg
    ))


def screen_menu():
    menu = Menu(root)
    root.config(menu=menu)

    # File menu
    file_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label='File', menu=file_menu)

    file_menu.add_command(label=" New ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + N', command=new)
    file_menu.add_command(label=" Save ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + S', command=save)
    file_menu.add_command(label=" Save As ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + Shift + S', command=save_as)
    file_menu.add_command(label=" Open ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + O', command=open_file)
    file_menu.add_separator(background='#0084BA')

    file_menu.add_command(label=" Exit ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + Esc', command=exit_app)

    # Edit menu
    edit_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label='Edit', menu=edit_menu)

    edit_menu.add_command(label=" Cut ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + X', command=cut)
    edit_menu.add_command(label=" Copy ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + C', command=copy)
    edit_menu.add_command(label=" Paste ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + V', command=paste)
    edit_menu.add_separator(background="#0084BA")

    edit_menu.add_command(label=" Undo ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + Z', command=undo)
    edit_menu.add_command(label=" Redo ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + U', command=redo)
    edit_menu.add_separator(background="#0084BA")

    edit_menu.add_command(label=" Select all ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + A', command=select_all)
    edit_menu.add_command(label=" Find ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + F', command=find_text)
    edit_menu.add_separator(background='#0084BA')

    edit_menu.add_command(label=" Insert date ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + D', command=insert_date)
    edit_menu.add_command(label=" Insert time ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', accelerator='Ctrl + Shift + T', command=insert_time)
    edit_menu.add_command(label=" Insert date and time ", background="#0084BA", foreground="white",
                          activebackground='black', font=('Calibri', 12), compound='left',
                          accelerator='Ctrl+ Shift + T', command=insertDateTime)
    edit_menu.add_separator(background='#0084BA')

    edit_menu.add_command(label=" Convert to Upper case ", background="#0084BA", foreground="white",
                          activebackground='black', font=('Calibri', 12), compound='left', command=upper_case,
                          accelerator='Ctrl + Shift + U')
    edit_menu.add_command(label=" Convert to Lower Case ", background="#0084BA", foreground="white",
                          activebackground='black', font=('Calibri', 12), compound='left', command=lower_case,
                          accelerator='Ctrl + Shift +  L')

    view_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label='View', menu=view_menu)
    view_menu.add_command(label=" Dark mode ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', command=dark_mode)

    view_menu.add_command(label=" Light mode ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', command=light_mode)
    view_menu.add_command(label=" Eye protection mode ", background="#0084BA", foreground="white",
                          activebackground='black', font=('Calibri', 12), compound='left', command=eye_protection_mode)

    view_menu.add_command(label=" Toggle Word Wrap ", background="#0084BA", foreground="white",
                          activebackground='black', font=('Calibri', 12), compound='left', command=toggle_word_wrap)

    text_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label='Text', menu=text_menu)

    text_menu.add_command(label=" Font Color ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', command=change_font_color)
    text_menu.add_command(label=" Change Font ", background="#0084BA", foreground="white", activebackground='black',
                          font=('Calibri', 12), compound='left', command=change_font_menu)
    text_menu.add_command(label=" Change font size ", background="#0084BA", foreground="white",
                          activebackground='black', font=('Calibri', 12), compound='left',
                          command=change_font_size_menu)
    text_menu.add_command(label=" Text background ", background="#0084BA", foreground="white", command=change_bg_color,
                          activebackground='black', font=('Calibri', 12), compound='left')
    text_menu.add_separator(background="#0084BA")

    text_menu.add_command(label=" Bold ", background="#0084BA", foreground="white", command=bold,
                          activebackground='black', font=('Calibri', 12), compound='left')
    text_menu.add_command(label=" Italic ", background="#0084BA", foreground="white", command=italic,
                          activebackground='black', font=('Calibri', 12), compound='left')
    text_menu.add_command(label=" Underline ", background="#0084BA", foreground="white", command=underline,
                          activebackground='black', font=('Calibri', 12), compound='left')
    text_menu.add_command(label=" Strike ", background="#0084BA", foreground="white", command=over_strike,
                          activebackground='black', font=('Calibri', 12), compound='left')

    about_menu = Menu(menu, tearoff=False)
    menu.add_cascade(label='About', menu=about_menu)

    about_menu.add_command(label=" About AText ", background="#0084BA", foreground="white", activebackground='black',
                           font=('Calibri', 12), compound='left', command=about)
    about_menu.add_command(label=" Help ", background="#0084BA", foreground="white", activebackground='black',
                           font=('Calibri', 12), compound='left', command=help)


def update_status_bar(statement):
    status_bar['text'] = statement


def WriteToFile(file):
    try:
        content = text.get(1.0, 'end')
        with open(file, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass


global filename


def save_as():
    input_file_name = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("All Files", "*.*"),
                                                              ("Text Documents", "*.txt"),
                                                              ("HTML", "*.html"), ("CSS", "*.css"),
                                                              ("JavaScript", "*.js")])

    if input_file_name:
        global filename
        filename = input_file_name
        x = ('{} - {}'.format(os.path.basename(filename), root.title()))
        root.title(x)

    return "break"


file_path = None


def new():
    global file_path

    message = messagebox.askyesno(
        "Are you sure?",
        "Do you want to save this file before creating a new one?"
    )

    if message:
        save()
        text.delete("1.0", END)

    else:
        text.delete("1.0", END)

    update_status_bar("New file created successfully")


def open_file():
    global file_path

    file_types = [
        ('Text Documents', "*.txt"),
        ('MS Word files', "*.docx"),
        ('All files', '*.*')
    ]

    file_path = askopenfilename(filetypes=file_types)

    if file_path == '':
        file_path = None
        return


    else:
        try:
            file1 = open(file_path, 'r')
            text.delete("1.0", END)
            data = file1.read()
            text.insert(END, data)
            root.title("AText - " + os.path.basename(file_path))
            file1.close()

        except FileNotFoundError:
            return

    update_status_bar(f'{file_path} has been open in this editor')


def save():
    global file_path

    file_types = [
        ('Text Documents', "*.txt"),
        ("MS Word files", '*.docx'),
        ('All files', '*.*')
    ]

    if file_path == None:
        file_path = asksaveasfilename(filetypes=file_types, defaultextension='.txt')

        if file_path == "":
            file_path = None

            return

        else:
            try:
                file1 = open(file_path, 'w')
                data = text.get("1.0", END)
                file1.write(data)
                root.title("AText" + os.path.basename(file_path))

            except FileNotFoundError:
                return


    else:
        file2 = open(file_path, 'w')
        data1 = text.get("1.0", END)
        file2.write(data1)
        root.title("AText" + os.path.basename(file_path))

    update_status_bar(f'{file_path} saved successfully')


def upper_case():
    content = text.get("1.0", END)
    text.delete("1.0", END)

    upper_content = content.upper()

    text.insert("1.0", upper_content)


def lower_case():
    content = text.get("1.0", END)
    text.delete("1.0", END)

    lower_content = content.lower()

    text.insert("1.0", lower_content)


def find_text():
    search_top_level = Toplevel(root)
    search_top_level.title('Find Text')
    search_top_level.transient(root)
    search_top_level.resizable(False, False)
    Label(search_top_level, text="Find:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_top_level, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_top_level, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                                                                                       padx=2, pady=2)
    Button(search_top_level, text="Find", underline=0, relief='solid',
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               text, search_top_level, search_entry_widget)
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


def dark_mode():
    shortcut_bar['bg'] = '#202020'

    bold_button['bg'] = '#202020'
    bold_button['fg'] = 'white'
    hover(bold_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    italic_button['bg'] = '#202020'
    italic_button['fg'] = 'white'
    hover(italic_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    underline_button['bg'] = '#202020'
    underline_button['fg'] = 'white'
    hover(underline_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    over_strike_button['bg'] = '#202020'
    over_strike_button['fg'] = 'white'
    hover(over_strike_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    cut_button['bg'] = '#202020'
    cut_button['fg'] = 'white'
    hover(cut_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    copy_button['bg'] = '#202020'
    copy_button['fg'] = 'white'
    hover(copy_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    paste_button['bg'] = '#202020'
    paste_button['fg'] = 'white'
    hover(paste_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    undo_button['bg'] = '#202020'
    undo_button['fg'] = 'white'
    hover(undo_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    redo_button['bg'] = '#202020'
    redo_button['fg'] = 'white'
    hover(redo_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    select_button['bg'] = '#202020'
    select_button['fg'] = 'white'
    hover(select_button, on_entrance='#202020', on_exit='#202020', entrance_fg='white', exit_fg='white')

    root.config(bg='#565454')
    status_bar.config(bg='black', fg='white')


def light_mode():
    shortcut_bar['bg'] = 'white'

    bold_button['bg'] = 'white'
    bold_button['fg'] = 'black'
    hover(bold_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    italic_button['bg'] = 'white'
    italic_button['fg'] = 'black'
    hover(italic_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    underline_button['bg'] = 'white'
    underline_button['fg'] = 'black'
    hover(underline_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    over_strike_button['bg'] = 'white'
    over_strike_button['fg'] = 'black'
    hover(over_strike_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    cut_button['bg'] = 'white'
    cut_button['fg'] = 'black'
    hover(cut_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    copy_button['bg'] = 'white'
    copy_button['fg'] = 'black'
    copy_button.config(highlightthickness=3, highlightbackground='black', default='active', highlightcolor='black')
    hover(copy_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    paste_button['bg'] = 'white'
    paste_button['fg'] = 'black'
    cut_button.config(highlightthickness=3, highlightbackground='black', default='active', highlightcolor='black')
    hover(paste_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    undo_button['bg'] = 'white'
    undo_button['fg'] = 'black'
    hover(undo_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    redo_button['bg'] = 'white'
    redo_button['fg'] = 'black'
    hover(redo_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')

    select_button['bg'] = 'white'
    select_button['fg'] = 'black'
    hover(select_button, on_entrance='#202020', on_exit='white', entrance_fg='white', exit_fg='black')

    root.config(bg='white')
    status_bar.config(bg='white', fg='black')


def eye_protection_mode():
    root.config(bg='#9EFFF3')
    shortcut_bar.config(bg='#9EFFF3')


def change_font(event=None):
    global current_font_family
    global current_font_size
    current_font_family = font_family.get()
    current_font_size = font_size.get()
    text.configure(font=(current_font_family, current_font_size))
    update_status_bar(f'Font changed to {current_font_family} and size is {current_font_size}')


def change_font_size_menu():
    messagebox.showinfo(
        "Change font size via the ComboBox",
        "You can change the font size via the Font size ComboBox in the toolbar"
    )


def change_font_menu():
    messagebox.showinfo(
        "Change font via the ComboBox",
        "You can change the font via the Font ComboBox in the toolbar"
    )


def change_font_color():
    color = colorchooser.askcolor()
    text.config(fg=color[1])


def change_bg_color():
    color = colorchooser.askcolor()
    text.config(bg=color[1])


def bold():
    text_property = font.Font(font=text['font'])

    if text_property.actual()['weight'] == 'normal':
        text.configure(font=(current_font_family, current_font_size, 'bold'))

    elif text_property.actual()['weight'] == 'italic':
        text.configure(font=(current_font_family, current_font_size, 'bold', 'italic'))

    elif text_property.actual()['weight'] == 'bold':
        text.configure(font=(current_font_family, current_font_size, 'normal'))

    elif text_property.actual()['weight'] == 'underline':
        text.configure(font=(current_font_family, current_font_size, 'bold', 'underline'))

    update_status_bar('Font style changed to bold')


def italic():
    text_property = font.Font(font=text['font'])

    if text_property.actual()['weight'] == 'normal':
        text.configure(font=(current_font_family, current_font_size, 'italic'))

    elif text_property.actual()['weight'] == 'italic':
        text.configure(font=(current_font_family, current_font_size, 'normal'))

    elif text_property.actual()['weight'] == 'bold':
        text.configure(font=(current_font_family, current_font_size, 'italic', 'bold'))

    elif text_property.actual()['weight'] == 'underline':
        text.configure(font=(current_font_family, current_font_size, 'italic', 'underline'))

    update_status_bar('Font style changed to italic')


def underline():
    text_property = font.Font(font=text['font'])

    if text_property.actual()['weight'] == 'normal':
        text.configure(font=(current_font_family, current_font_size, 'underline'))

    elif text_property.actual()['weight'] == 'underline':
        text.configure(font=(current_font_family, current_font_size, 'normal'))

    elif text_property.actual()['weight'] == 'italic':
        text.configure(font=(current_font_family, current_font_size, 'normal', 'italic'))

    elif text_property.actual()['weight'] == 'bold':
        text.configure(font=(current_font_family, current_font_size, 'underline', 'bold'))

    update_status_bar('Font style changed to Underline')


def over_strike():
    text_property = font.Font(font=text['font'])

    if text_property.actual()['weight'] == 'normal':
        text.configure(font=(current_font_family, current_font_size, 'overstrike'))

    elif text_property.actual()['weight'] == 'overstrike':
        text.configure(font=(current_font_family, current_font_size, 'normal'))

    elif text_property.actual()['weight'] == 'italic':
        text.configure(font=(current_font_family, current_font_size, 'overstrike', 'italic'))

    elif text_property.actual()['weight'] == 'bold':
        text.configure(font=(current_font_family, current_font_size, 'overstrike', 'bold'))

    update_status_bar('Font Striked')


def toggle_word_wrap():
    if text['wrap'] == 'word':
        text.config(wrap='none')

    elif text['wrap'] == 'none':
        text.config(wrap='word')

    update_status_bar("Word wrap has been toggled")


def about():
    messagebox.showinfo(
        "About",
        "AText is created with hard work by Amey V"
    )


def help():
    messagebox.showinfo(
        "Help",
        """The functions are: \n
        You have several menus in this editor.\n
        You have many functions in the toolbar. \n
        You can change the modes, colors and fonts.\n
        You have many more features!"""
    )


def last_character(event):
    type_label['text'] = f'Last character typed: {event.char}'


def update_char_length(event=None):
    string_in_text = text.get('1.0', 'end-1c')
    string_length = len(string_in_text)
    chars_label['text'] = f'Total Characters: {string_length}'


def count(event):
    (line, letter) = map(int, event.widget.index("end-1c").split("."))
    words = len(text.get("1.0", "end-1c").split())

    lines_label['text'] = f'Total Lines: {line}'
    words_label['text'] = f'Total Words: {words}'


counter = 66600
running = False


def counter_label(event=None):
    def count_time():
        if running:
            global counter

            if counter == 66600:
                display = "Working time: 00:00:00"

            else:
                tt = datetime.fromtimestamp(counter)
                string = tt.strftime("Working time: " + "%H:%M:%S")
                display = string

            time_label['text'] = display
            time_label.after(1000, count_time)
            counter += 1

    count_time()


def exit_app():
    message = messagebox.askyesno(
        "Do you want to exit?",
        "Do you want to save the file? "
    )

    if message:
        save_as()
        root.quit()

    else:
        root.quit()


def start(event=None):
    global running
    running = True
    counter_label(time_label)


def insert_date():
    today = date.today().strftime("%A, %d.%B %Y")
    text.insert("1.0", today)
    update_status_bar("Date has been inserted to the file")


def insert_time():
    today = time.strftime("%H:%M Uhr ")
    text.insert("1.0", today)
    update_status_bar("Time has been inserted to the file")


def insertDateTime():
    insert_date()
    insert_time()
    update_status_bar("Time and date has been added to the file.")


def cut():
    text.event_generate("<<Cut>>")
    update_status_bar("Text cut")


def copy():
    text.event_generate("<<Copy>>")
    update_status_bar("Text copied to clipboard")


def paste():
    text.event_generate("<<Paste>>")
    update_status_bar("Text pasted from clipboard")


def undo():
    text.edit_undo()
    update_status_bar("Undo Successful")


def redo():
    text.edit_redo()
    update_status_bar("Redo Successful")


def select_all():
    text.event_generate("<<SelectAll>>")
    update_status_bar("Everything has been selected.")


root = Tk()
root.resizable(False, False)
root.title("AText")
root.geometry("900x600")

frame = Frame(root, bd=3, bg='white', highlightthickness=10, highlightbackground='black')
frame.place(relx=0.5, rely=0.11, relwidth=0.85, relheight=0.85, anchor='n')

text = ScrolledText(frame, height=100, width=100, padx=3, pady=5, undo=True, wrap='word')
text.pack()

default_font_family = "Calibri"
default_font_size = 14

shortcut_bar = Frame(root, height=35, bg='white')
shortcut_bar.pack(expand='no', fill='x')

fonts = font.families()
font_family = StringVar()
font_box = ttk.Combobox(shortcut_bar, width=30, textvariable=font_family, state='readonly')
font_box['values'] = fonts
font_box.current(fonts.index("Calibri"))
font_box.place(x=25, y=5)

current_font_family = 'Calibri'
current_font_size = 14

size_var = IntVar()
size = tuple(range(5, 90))
font_size = ttk.Combobox(shortcut_bar, width=14, textvariable=size_var, state='readonly')
font_size['values'] = size
font_size.current(size.index(14))
font_size.place(x=250, y=5)

lines_label = Label(root, text='Total lines: 0', fg='black', font=('Calibri', 12), relief='ridge', width=15, bg='white')
lines_label.place(x=70, y=40)

chars_label = Label(root, text='Total Characters: 0', fg='black', font=('Calibri', 12), relief='ridge', width=20,
                    bg='white')
chars_label.place(x=200, y=40)

words_label = Label(root, text='Total Words: 0', fg='black', font=('Calibri', 12), relief='ridge', width=15, bg='white')
words_label.place(x=370, y=40)

time_label = Label(root, text='Working time: 00:00', fg='black', font=('Calibri', 12), relief='ridge', width=20,
                   bg='white')
time_label.place(x=500, y=40)

type_label = Label(root, text='Last character typed: ', fg='black', font=('Calibri', 12), relief='ridge', width=20,
                   bg='white')
type_label.place(x=670, y=40)

status_bar = Label(root, text='Status Bar', fg='black', font=("Calibri", 12, 'italic'))
status_bar.place(x=1, y=580)
status_text = status_bar['text']

bold_button = Button(shortcut_bar, text='B', relief=FLAT, fg='black', font=('Arial', 12, 'bold'), bg='white',
                     height=1, command=bold)
hover(bold_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
bold_button.place(x=380, y=(-1))

italic_button = Button(shortcut_bar, text='I', relief=FLAT, fg='black', font=('Arial', 12, 'italic'), bg='white',
                       command=italic)
hover(italic_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
italic_button.place(x=410, y=(-1))

underline_button = Button(shortcut_bar, text='U', relief=FLAT, fg='black', font=('Arial', 12, 'underline'), bg='white',
                          command=underline)
hover(underline_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
underline_button.place(x=435, y=(-1))

over_strike_button = Button(root, text='Strike', relief=FLAT, fg='black', font=('Arial', 12, 'overstrike'), bg='white',
                            command=over_strike)

hover(over_strike_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
over_strike_button.place(x=470, y=(-1))

cut_button = Button(root, text='Cut', relief=FLAT, fg='black', font=('Arial', 12), bg='white', command=cut, height=0,
                    highlightthickness=3, highlightbackground='black', default='active', highlightcolor='black')
hover(cut_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
cut_button.place(x=530, y=(-1))

copy_button = Button(root, text='Copy', relief=FLAT, fg='black', font=('Arial', 12), bg='white', command=copy, height=0,
                     highlightthickness=3, highlightbackground='black', default='active', highlightcolor='black')
hover(copy_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
copy_button.place(x=580, y=(-1))

paste_button = Button(root, text='Paste', relief=FLAT, fg='black', font=('Arial', 12), bg='white', command=paste,
                      height=0, highlightthickness=3, highlightbackground='black', default='active',
                      highlightcolor='black')
hover(paste_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
paste_button.place(x=640, y=(-1))

undo_button = Button(shortcut_bar, text='⬅', relief=FLAT, fg='black', font=('Arial', 15), bg='white',
                     command=undo)
hover(undo_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
undo_button.place(x=700, y=-3)

redo_button = Button(shortcut_bar, text='➡', relief=FLAT, fg='black', font=('Arial', 15), bg='white',
                     command=redo)
hover(redo_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
redo_button.place(x=740, y=-3)

select_button = Button(shortcut_bar, text='Select All', relief=FLAT, fg='black', font=('Arial', 12), bg='white',
                       command=select_all, highlightthickness=3, highlightbackground='black', default='active',
                       highlightcolor='black')
hover(select_button, on_entrance='#0084BA', on_exit='white', entrance_fg='white', exit_fg='black')
select_button.place(x=780, y=0)
# Bindings

bindtags = list(text.bindtags())
bindtags.insert(2, "custom")
text.bindtags(tuple(bindtags))
text.bind_class("custom", "<Key>", count)

font_box.bind("<<ComboboxSelected>>", change_font)
font_size.bind("<<ComboboxSelected>>", change_font)

text.bind('<KeyPress>', update_char_length)
text.bind('<KeyRelease>', update_char_length)

start(time_label)

text.bind("<Key>", last_character)

text.config(font=(default_font_family, default_font_size))

screen_menu()
root.protocol("WM_DELETE_WINDOW", exit_app)
root.mainloop()
