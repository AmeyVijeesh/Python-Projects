from tkinter import *
from tkinter import messagebox
import requests
import webbrowser
import calendar
from datetime import datetime


def weather_app():
    root = Toplevel()
    root.geometry("366x650")
    root.title("Weather")

    def formatResponse(weather):
        try:
            name = weather['name']
            country = weather['sys']['country']
            description = weather['weather'][0]['description']
            temp = weather['main']['temp']
            temp_min = weather['main']['temp_min']
            temp_max = weather['main']['temp_max']
            feels_temp = weather['main']['feels_like']
            humidity = weather['main']['humidity']

            result = "City: %s \n Country: %s \nConditions: %s \nTemperature (°F): %s \n Min temp: %s \n " \
                     " Max Temp: %s \n  Feels Like: %s \nHumidity: %s" % \
                     (name, country, description, temp, temp_min, temp_max, feels_temp, humidity)
        except KeyError:
            result = "Please retry: "

        return result

    def getWeather(city):
        weather_key = 'c03eeb08b471c10ca8057b5078e9ca0a'
        url = "http://api.openweathermap.org/data/2.5/weather"
        parameters = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
        response = requests.get(url, params=parameters)
        weather = response.json()

        label['text'] = formatResponse(weather)

    frame1 = Frame(root, highlightbackground="#00D4FF", highlightthickness=8)
    frame1.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.1, anchor="n")

    frame2 = Frame(root, bg='#00D4FF', bd=5)
    frame2.place(relx=0.5, rely=0.25, relwidth=0.9, relheight=0.65, anchor="n")

    label = Label(frame2, justify="center", font=("Calibri", 17), text="Enter the city: ")
    label.place(relwidth=1, relheight=1)

    user_entry = Entry(frame1)
    user_entry.place(x=10, y=15)

    enter_btn = Button(frame1, text='Search', width=7, command=lambda: getWeather(user_entry.get()))
    enter_btn.place(relx=0.68, rely=0.2, relwidth=0.3, relheight=0.6)

    root.mainloop()


def on_screen_keyboard():
    root = Toplevel()
    root.geometry("366x650")
    root.resizable(False, False)
    root.title("On screen Keyboard")

    txt = Text(root, width=44, height=30, wrap=WORD, font='Arial')
    txt.place(x=3, y=50)
    txt.focus_set()

    Label(root, text='', height=32).grid(row=1, column=20)

    buttons = [
        '~', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '←',
        '"', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', '[', ']',
        '⬆️', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '?',
        '!', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ':',
    ]

    varRow = 6
    varCol = 0

    global caps_lock

    caps_lock = False
    letter_buttons = []

    def is_letter(s):
        return len(s) == 1 and 'a' <= s <= 'z'

    def buttonClick(user_input):
        global caps_lock

        if user_input == '⬆️':
            caps_lock = not caps_lock
            for btn in letter_buttons:
                text = btn['text']
                btn['text'] = text.upper() if caps_lock else text.lower()
        else:
            if user_input == ' Space ':
                txt.insert(INSERT, ' ')
            elif user_input == '←':
                backspace()
            elif user_input == ' Return ':
                txt.insert(INSERT, '\n')
            else:
                if is_letter(user_input):
                    user_input = user_input.upper() if caps_lock else user_input.lower()
                txt.insert(INSERT, user_input)

    def backspace():
        txt.delete('insert-1chars', INSERT)

    space_btn = Button(root, width=20, text=' Space ', command=lambda: buttonClick(' Space '))
    space_btn.place(x=50, y=620)

    return_btn = Button(root, width=6, text=' ⏎ ', command=lambda: buttonClick(' Return '))
    return_btn.place(x=250, y=620)

    for button in buttons:
        cmd = lambda x=button: buttonClick(x)

        if button != ' Space ':
            btn = Button(root, text=button, width=3,
                         command=cmd)
            btn.grid(row=varRow, column=varCol)
            if is_letter(button):
                letter_buttons.append(btn)

        if button == ' Space ':
            Button(root, text=button, command=cmd).grid(row=6, columnspan=16)
        varCol += 1

        if varCol > 11 and varRow >= 4:
            varCol = 0
            varRow += 1

    root.mainloop()


def calculator():
    root = Toplevel()
    root.geometry("366x650")
    root.configure(bg='black')
    root.title("Calculator")

    global expression
    expression = ""

    def click(no):
        global expression
        expression = expression + str(no)
        equation.set(expression)

    def show_result():
        try:
            global expression, answer

            answer = str(eval(expression))
            equation.set(answer)

            expression = ""

        except ZeroDivisionError and SyntaxError:
            messagebox.showerror("Wrong expression",
                                 "This expression can't be evaluated")

    def clear():
        global expression
        expression = ""
        equation.set("")

    equation = StringVar()

    user_input = Entry(root, width=20, font=('Calibri', 17), state='readonly', textvariable=equation)
    user_input.place(x=65, y=25)

    frame = Frame(root, bg='white')
    frame.place(relx=0.5, rely=0.10, relwidth=0.9, relheight=0.88, anchor="n")

    btn1 = Button(root, text="1", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(1))
    btn1.place(x=60, y=85)

    btn2 = Button(root, text="2", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(2))
    btn2.place(x=150, y=85)

    btn3 = Button(root, text="3", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(3))
    btn3.place(x=240, y=85)

    btn4 = Button(root, text="4", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(4))
    btn4.place(x=60, y=185)

    btn5 = Button(root, text="5", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(5))
    btn5.place(x=150, y=185)

    btn6 = Button(root, text="6", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(6))
    btn6.place(x=240, y=185)

    btn7 = Button(root, text="7", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(7))
    btn7.place(x=60, y=285)

    btn8 = Button(root, text="8", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(8))
    btn8.place(x=150, y=285)

    btn9 = Button(root, text="9", width=7, height=3, highlightbackground='#000000', fg='black',
                  command=lambda: click(9))
    btn9.place(x=240, y=285)

    btn_zero = Button(root, text='0', width=7, height=3, highlightbackground='#000000', fg='black',
                      command=lambda: click(0))
    btn_zero.place(x=60, y=385)

    btn_clr = Button(root, text="Clear", width=17, height=3, highlightbackground='#000000', fg='black',
                     command=clear)
    btn_clr.place(x=150, y=385)

    btn_add = Button(root, text="+", width=7, height=3, highlightbackground='#000000', fg='black',
                     command=lambda: click("+"))
    btn_add.place(x=60, y=485)

    btn_sub = Button(root, text="-", width=7, height=3, highlightbackground='#000000', fg='black',
                     command=lambda: click("- "))
    btn_sub.place(x=150, y=485)

    btn_multiply = Button(root, text="x", width=7, height=3, highlightbackground='#000000', fg='black',
                          command=lambda: click("* "))
    btn_multiply.place(x=240, y=485)

    btn_div = Button(root, text="/", width=7, height=3, highlightbackground='#000000', fg='black',
                     command=lambda: click("/ "))
    btn_div.place(x=60, y=575)

    btn_equal = Button(root, text="=", width=7, height=3, highlightbackground='#000000', fg='black',
                       command=show_result)
    btn_equal.place(x=150, y=575)

    btn_point = Button(root, text=".", width=7, height=3, highlightbackground='#000000', fg='black',
                       command=lambda: click(". "))
    btn_point.place(x=240, y=575)

    root.mainloop()


def web_browser():
    root = Toplevel()
    root.geometry("366x650")
    root.title("Web Surf Browser")

    canvas = Canvas(root)

    bg_img = PhotoImage(file='img.png')
    canvas.create_image(0, 0, image=bg_img, anchor=NW)
    canvas.pack(fill='both', expand=True)

    input_entry = Entry(canvas, width=24, font=('Calibri', 14))
    input_entry.place(x=30, y=100)

    def search():
        user_input = input_entry.get()

        if '.com' in user_input or '.net' in user_input or '.us' in user_input or '.org' in user_input:
            webbrowser.open("https://www." + user_input)

        else:
            webbrowser.open("https://www.bing.com/search?q=" + user_input)

    search_btn = Button(canvas, text="⏎", width=7, height=2, command=search)
    search_btn.place(x=270, y=96)

    python_btn = Button(canvas, text='Python', width=7, height=2, highlightbackground='#778899',
                        command=lambda: webbrowser.open('https://python.org'))
    python_btn.place(x=50, y=350)

    google_btn = Button(canvas, text='Google', width=7, height=2, highlightbackground='#778899',
                        command=lambda: webbrowser.open('https://google.com'))
    google_btn.place(x=150, y=350)

    github_btn = Button(canvas, text='Github', width=7, height=2, highlightbackground='#778899',
                        command=lambda: webbrowser.open('https://github.com'))
    github_btn.place(x=250, y=350)

    outlook_btn = Button(canvas, text='Outlook', width=7, height=2, highlightbackground='#778899',
                         command=lambda: webbrowser.open('https://outlook.com'))
    outlook_btn.place(x=150, y=450)

    gmail_btn = Button(canvas, text='Gmail', width=7, height=2, highlightbackground='#778899',
                       command=lambda: webbrowser.open('https://mail.google.com/mail/u/0/#inbox'))
    gmail_btn.place(x=50, y=450)

    amazon_btn = Button(canvas, text='Youtube', width=7, height=2, highlightbackground='#778899',
                        command=lambda: webbrowser.open('https://youtube.com'))
    amazon_btn.place(x=250, y=450)

    translate_btn = Button(canvas, text='Translator', width=7, height=2, highlightbackground='#778899',
                           command=lambda: webbrowser.open('https://bing.com/translate'))
    translate_btn.place(x=50, y=550)

    maps_btn = Button(canvas, text='Maps', width=7, height=2, highlightbackground='#778899',
                      command=lambda: webbrowser.open('https://bing.com/maps'))
    maps_btn.place(x=150, y=550)

    amazon_btn = Button(canvas, text='Amazon', width=7, height=2, highlightbackground='#778899',
                        command=lambda: webbrowser.open('https://amazon.com'))
    amazon_btn.place(x=250, y=550)

    root.mainloop()


def calendar_app():
    root = Toplevel()
    root.geometry("366x650")
    root.resizable(False, False)
    root.title("Calendar")

    def find_calendar():
        month = int(month_spinbox.get())
        year = int(var.get())

        month_calendar = calendar.month(year, month)

        display_label['text'] = ''
        display_label['text'] = month_calendar

    frame2 = Frame(root, highlightbackground='black', bd=5, highlightthickness=4)
    frame2.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.90, anchor="n")

    display_label = Label(root, text='', font=('Calibri', 14))
    display_label.place(x=100, y=350)

    month_label = Label(root, text='Month: ')
    month_label.place(x=50, y=105)

    month_spinbox = Spinbox(root, from_=1, to=12, state='readonly', width=14)
    month_spinbox.place(x=150, y=100)

    year_label = Label(root, text='Year: ')
    year_label.place(x=50, y=185)

    go_btn = Button(root, text='Go', width=5, command=find_calendar)
    go_btn.place(x=160, y=250)

    var = IntVar()
    var.set(2021)
    year_spinbox = Spinbox(root, from_=1900, to=3000, width=14, textvariable=var)
    year_spinbox.place(x=150, y=180)

    root.mainloop()


counter = 66600
running = False


def stopwatch():
    root = Toplevel()
    root.geometry("366x650")
    root.configure(bg='#333333')
    root.title("Stopwatch")

    def count_time(event=None):
        def count():
            if running:
                global counter

                if counter == 66600:
                    display = "00:00:00"

                else:
                    tt = datetime.fromtimestamp(counter)
                    string = tt.strftime("%H:%M:%S")
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
        reset_btn['state'] = 'normal'

    def stop():
        global running
        start_btn['state'] = 'normal'
        stop_btn['state'] = 'disabled'
        reset_btn['state'] = 'normal'
        running = False

    def reset(label):
        global counter
        counter = 66600

        if not running:
            reset_btn['state'] = 'disabled'
            label['text'] = '00:00:00'

        else:
            label['text'] = 'Starting...'

    time_label = Label(root, font=('Arial', 25, 'bold'), text='00:00:00')
    time_label.place(x=130, y=200)
    stop_btn = Button(root, text='Stop Counting', font=('Arial', 15), relief='ridge', command=stop, state='disabled')
    stop_btn.place(x=130, y=500)

    start_btn = Button(root, text='Start Counting', relief='ridge', state='normal',
                       command=start)
    start_btn.place(x=130, y=300)

    reset_btn = Button(root, text='Reset Counting', relief='ridge', state='disabled',
                       command=lambda: reset(time_label))
    reset_btn.place(x=130, y=350)
    stop_btn.place(x=130, y=400)
    root.mainloop()

