# Importing tkinter for GUI
from tkinter import *
from tkinter.font import Font
# These are the imports for scraping the information from the webpage
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup

global dic
dic = PyDictionary()


def init():
    """This includes the details of the mainwindow and fonts used here"""
    global root
    root = Tk()
    root.config(bg='#FFFFFF')  # Pure white
    root.title('Dictionary')
    root.geometry('500x350')
    root.resizable(False, False)

    global title_font
    global input_font
    global button_font
    global unavailable_font
    global meaning_font
    global tab_font
    title_font = Font(size=30, family='Bahnschrift')
    unavailable_font = Font(size=20, family='Bahnschrift Light')
    input_font = Font(size=20, family='Corbel')
    button_font = Font(size=15, family='Franklin Gothic Medium')
    tab_font = Font(size=15, family='Bahnschrift Light')
    meaning_font = Font(size=15)


def menu():
    """The main definition"""
    init()
    global not_available_message
    global search_input

    def input():
        """In this definition, the user inputs the word to search for the meaning"""

        global search_input
        global tab_frame
        global textbox
        global meaning_tab
        global synonym_tab
        global antonym_tab
        global not_available_message
        global synonym
        global antonym
        word = search_input.get()
        synonym = []
        antonym = []
        meaning = dic.meaning(word)

        url = 'https://www.synonym.com/synonyms/' + word  # The website in which the meanings are scraped
        page = requests.get(url)

        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            syn = soup.find('div', {'class': 'card full-width mdc-card type-synonym'}).find('div', {
                'class': 'card-content'}).findAll('a')
            for x in syn:
                synonym.append(x.text)
            for x in range(len(synonym)):
                synonym[x] = ''.join(synonym[x].replace('\n', '').split())
        except:
            synonym = ['NONE']
        try:
            ant = soup.find('div', {'class': 'card full-width mdc-card type-antonym'}).find('div', {
                'class': 'card-content'}).findAll('a')
            for x in ant:
                antonym.append(x.text)
            for x in range(len(antonym)):
                antonym[x] = ''.join(antonym[x].replace('\n', '').split())
        except:
            antonym = ['NONE']

        if meaning == None:
            print('The word is unavailable')

            not_available_message = Label(
                root,
                text='word not available',
                font=unavailable_font,
                bg='white',
                fg='#FF7D7D'
            )

            not_available_message.place(x=135, y=290)
            try:  # try if it is possible
                tab_frame.place_forget()
                textbox.place_forget()
                meaning_tab.place_forget()
                synonym_tab.place_forget()
                antonym_tab.place_forget()
                root.geometry('500x350')

            except:
                pass

        else:
            global key
            global values
            try:
                synonym_tab.place_forget()
                meaning_tab.place_forget()
                antonym_tab.place_forget()
            except:
                pass

            root.geometry('500x750')
            try:
                not_available_message.place_forget()
            except:
                pass

            def meaning_tab_on_enter(e):
                if meaning_tab['state'] == NORMAL:
                    meaning_tab['background'] = '#1A73E8'
                    meaning_tab['fg'] = 'white'

            def meaning_tab_on_leave(e):
                if meaning_tab['state'] == NORMAL:
                    meaning_tab['background'] = '#F1F1F3'
                    meaning_tab['fg'] = '#656567'

            def synonym_tab_on_enter(e):
                if synonym_tab['state'] == NORMAL:
                    synonym_tab['background'] = '#1A73E8'
                    synonym_tab['fg'] = 'white'

            def synonym_tab_on_leave(e):
                if synonym_tab['state'] == NORMAL:
                    synonym_tab['background'] = '#F1F1F3'
                    synonym_tab['fg'] = '#656567'

            def antonym_tab_on_enter(e):
                if antonym_tab['state'] == NORMAL:
                    antonym_tab['background'] = '#1A73E8'
                    antonym_tab['fg'] = 'white'

            def antonym_tab_on_leave(e):
                if antonym_tab['state'] == NORMAL:
                    antonym_tab['background'] = '#F1F1F3'
                    antonym_tab['fg'] = '#656567'

            tab_frame = Frame(
                root,
                width=454,
                height=351,
                bg='#1A73E8'
            )

            def synonym_func():
                """The synonym tab"""
                global meaning_tab
                global antonym_tab
                global synonym_tab
                global textbox  #
                meaning_tab.place_forget()
                antonym_tab.place_forget()
                synonym_tab.place_forget()
                meaning_tab.config(bg='#F1F1F3', fg='#656567', state=NORMAL, pady=1)
                antonym_tab.config(bg='#F1F1F3', fg='#656567', state=NORMAL, pady=1)
                synonym_tab.config(bg='#1A73E8', fg='white', state=DISABLED,
                                   pady=3)
                meaning_tab.place(x=24, y=310)
                synonym_tab.place(x=174, y=310)
                antonym_tab.place(x=325, y=310)
                meaning_tab.bind("<Enter>", meaning_tab_on_enter)
                meaning_tab.bind("<Leave>", meaning_tab_on_leave)
                synonym_tab.bind("<Enter>", synonym_tab_on_enter)
                synonym_tab.bind("<Leave>", synonym_tab_on_leave)
                antonym_tab.bind("<Enter>", antonym_tab_on_enter)
                antonym_tab.bind("<Leave>", antonym_tab_on_leave)

                textbox.place_forget()
                textbox.config(state=NORMAL)
                textbox.delete(0.0, END)
                textbox.place(x=24, y=357)

                for i in synonym:
                    textbox.insert(END, ('\u21D2  ' + i + '\n'))

                textbox.config(state=DISABLED)

            def meaning_func():
                global meaning_tab
                global antonym_tab
                global synonym_tab
                global textbox
                global key
                global values
                meaning_tab.place_forget()
                antonym_tab.place_forget()
                synonym_tab.place_forget()
                meaning_tab.config(bg='#1A73E8', fg='white', state=DISABLED,
                                   pady=3)
                antonym_tab.config(bg='#F1F1F3', fg='#656567', state=NORMAL, pady=1)
                synonym_tab.config(bg='#F1F1F3', fg='#656567', state=NORMAL, pady=1)
                meaning_tab.place(x=24, y=310)
                synonym_tab.place(x=174, y=310)
                antonym_tab.place(x=325, y=310)
                meaning_tab.bind("<Enter>", meaning_tab_on_enter)
                meaning_tab.bind("<Leave>", meaning_tab_on_leave)
                synonym_tab.bind("<Enter>", synonym_tab_on_enter)
                synonym_tab.bind("<Leave>", synonym_tab_on_leave)
                antonym_tab.bind("<Enter>", antonym_tab_on_enter)
                antonym_tab.bind("<Leave>", antonym_tab_on_leave)
                textbox.grid_forget()
                textbox.config(state=NORMAL)
                textbox.delete(0.0, END)
                textbox.place(x=24, y=357)

                textbox.tag_configure('highlightline', background='white', foreground='black',
                                      font='helvetica 14 italic', relief='raised')

                for x in range(len(key)):
                    textbox.insert(END, key[x] + '\n',
                                   'highlightline')

                    for x1 in values[x]:
                        textbox.insert(END, '\u21D2  ' + x1 + '\n')
                    textbox.insert(END, '\n')
                textbox.config(state=DISABLED)

            def antonym_func():
                """The antonym function"""
                global meaning_tab
                global antonym_tab
                global synonym_tab
                global textbox
                meaning_tab.place_forget()
                antonym_tab.place_forget()
                synonym_tab.place_forget()
                meaning_tab.config(bg='#F1F1F3', fg='#656567', state=NORMAL, pady=1)
                antonym_tab.config(bg='#1A73E8', fg='white', state=DISABLED,
                                   pady=3)
                synonym_tab.config(bg='#F1F1F3', fg='#656567', state=NORMAL, pady=1)
                meaning_tab.place(x=24, y=310)
                synonym_tab.place(x=174, y=310)
                antonym_tab.place(x=325, y=310)
                meaning_tab.bind("<Enter>", meaning_tab_on_enter)
                meaning_tab.bind("<Leave>", meaning_tab_on_leave)
                synonym_tab.bind("<Enter>", synonym_tab_on_enter)
                synonym_tab.bind("<Leave>", synonym_tab_on_leave)
                antonym_tab.bind("<Enter>", antonym_tab_on_enter)
                antonym_tab.bind("<Leave>", antonym_tab_on_leave)

                textbox.grid_forget()
                textbox.config(state=NORMAL)
                textbox.delete(0.0, END)
                textbox.place(x=24, y=357)

                for i in antonym:
                    textbox.insert(END, ('\u21D2  ' + i + '\n'))

                textbox.config(state=DISABLED)

            meaning_tab = Button(
                root,
                text='MEANING',
                bg='#1A73E8',
                fg='white',
                font=tab_font,
                relief=FLAT,
                padx=21.9,
                pady=3,
                disabledforeground='white',
                state=DISABLED,
                command=meaning_func,
                activebackground='#1A73E8',
                activeforeground='white'
            )
            synonym_tab = Button(
                root,
                text='SYNONYM',
                bg='#F1F1F3',
                fg='#656567',
                font=tab_font,
                relief=FLAT,
                padx=21.9,
                pady=1,
                disabledforeground='white',
                command=synonym_func,
                activebackground='#1A73E8',
                activeforeground='white'
            )
            antonym_tab = Button(
                root,
                text='ANTONYM',
                bg='#F1F1F3',
                fg='#656567',
                font=tab_font,
                relief=FLAT,
                padx=22,
                pady=1,
                disabledforeground='white',
                command=antonym_func,
                activebackground='#1A73E8',
                activeforeground='white'
            )
            values = list(dic.meaning(word).values())
            key = list(dic.meaning(word))

            for x in range(len(values)):
                for h in range(len(values[x])):
                    values[x][h] = values[x][h].replace('(', '')
            textbox = Text(
                root,
                bg='white',
                width=40,
                height=15,
                fg='#757575',
                relief=FLAT,
                borderwidth=0,
                padx=5,
                font=meaning_font
            )

            textbox.tag_configure(
                'highlightline',
                background='white',
                foreground='black',
                font='helvetica 14 italic',
                relief='raised'
            )

            for x in range(len(key)):
                textbox.insert(END, key[x] + '\n', 'highlightline')

                for m1 in values[x]:
                    textbox.insert(END, '\u21D2  ' + m1 + '\n')
                textbox.insert(END, '\n')

            tab_frame.place(x=22, y=355)
            textbox.config(state=DISABLED)
            textbox.place(x=24, y=357)
            meaning_tab.place(x=24, y=310)
            synonym_tab.place(x=174, y=310)
            antonym_tab.place(x=325, y=310)
            meaning_tab.bind("<Enter>", meaning_tab_on_enter)
            meaning_tab.bind("<Leave>", meaning_tab_on_leave)
            synonym_tab.bind("<Enter>", synonym_tab_on_enter)
            synonym_tab.bind("<Leave>", synonym_tab_on_leave)
            antonym_tab.bind("<Enter>", antonym_tab_on_enter)
            antonym_tab.bind("<Leave>", antonym_tab_on_leave)

    def on_click(event):
        search_input.configure(state=NORMAL)
        search_input.delete(0, END)
        search_input.unbind('<Button-1>', on_click_id)

    def button_on_enter(e):
        if submit_button['state'] == NORMAL:
            submit_button['background'] = '#1A73E8'
            submit_button['fg'] = 'white'

    def button_on_leave(e):
        if submit_button['state'] == NORMAL:
            submit_button['background'] = 'white'
            submit_button['fg'] = '#1A73E8'

    title = Label(
        root,
        text='Python Dictionary',
        font=title_font,
        bg='white',
        fg='#757575'
    )

    search_frame = Frame(
        root,
        width=342,
        height=64,
        background='#1A73E8',
        borderwidth=1
    )

    search_input = Entry(
        root,
        disabledbackground='white',
        font=input_font,
        borderwidth=0,
        fg='#757575',
        bg='white',
        relief=FLAT,
        justify=CENTER,
        width=24,
        insertbackground='#757575',
        disabledforeground='#757575'
    )

    submit_button_frame = Frame(
        root,
        width=344,
        height=64,
        background='#1A73E8')

    submit_button = Button(
        root,
        activebackground='#1A73E8',
        activeforeground='white',
        fg='#1A73E8',
        text='SEARCH',
        font=button_font,
        pady=9,
        width=30,
        bg='white',
        relief=FLAT,
        command=input)

    title.place(x=100, y=20)
    search_frame.place(x=80, y=130)
    search_input.place(x=82, y=132, height=60)
    search_input.insert(0, 'Type your word:')
    search_input.configure(state=DISABLED)
    submit_button_frame.place(x=79, y=210)
    submit_button.place(x=81, y=212)
    on_click_id = search_input.bind('<Button-1>', on_click)
    submit_button.bind("<Enter>", button_on_enter)
    submit_button.bind("<Leave>", button_on_leave)


if __name__ == '__main__':
    menu()
    root.mainloop()

# End of code
