from tkinter import *
import random
import sqlite3
import time
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


def loginPage(login_data):
    signup_page.destroy()
    global login_window
    login_window = Tk()
    login_window.title('Quiz App Login')
    login_window.resizable(False, False)

    user_name = StringVar()
    password = StringVar()

    login_canvas = Canvas(login_window, width=720, height=440, bg="white")
    login_canvas.pack()

    background_image = PhotoImage(file="tree.png")
    login_canvas.create_image(2, 1, image=background_image, anchor=NW)

    login_frame = Frame(login_canvas, bg="white")
    login_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    title = Label(login_frame, text="Quiz App Login", fg="foreground_black", bg="white")
    title.config(font='calibri 40')
    title.place(relx=0.2, rely=0.1)

    # USER NAME
    username_label = Label(login_frame, text="Username", fg='foreground_black', bg='white')
    username_label.place(relx=0.21, rely=0.4)
    username_entry = Entry(login_frame, bg='white', fg='foreground_black', textvariable=user_name)
    username_entry.config(width=42)
    username_entry.place(relx=0.31, rely=0.4)

    # PASSWORD
    password_label = Label(login_frame, text="Password", fg='foreground_black', bg='white')
    password_label.place(relx=0.215, rely=0.5)
    password_entry = Entry(login_frame, bg='white', fg='foreground_black', textvariable=password, show="*")
    password_entry.config(width=42)
    password_entry.place(relx=0.31, rely=0.5)

    def check():
        for a, b, c, d in login_data:
            if b == username_entry.get() and c == password_entry.get():
                print(login_data)

                menu(a)
                break
        else:
            error = Label(login_frame, text="Wrong Username or Password!", fg='foreground_black', bg='white')
            error.place(relx=0.37, rely=0.7)

    login_button = Button(login_frame, text='Login', padx=5, pady=5, width=5, command=check, fg="white", bg="foreground_black")
    login_button.configure(width=15, height=1, activebackground="#33B5E5", relief=FLAT)
    login_button.place(relx=0.4, rely=0.6)

    login_window.mainloop()


def signUpPage():
    root.destroy()
    global signup_page
    signup_page = Tk()
    signup_page.title('Quiz App signup')
    signup_page.resizable(False, False)

    name_entry = StringVar()
    username = StringVar()
    password = StringVar()
    country = StringVar()


    signup_canvas = Canvas(signup_page, width=720, height=440)
    signup_canvas.pack()

    image = PhotoImage(file="sun.png")
    signup_canvas.create_image(2, 1, image=image, anchor=NW)

    signup_frame = Frame(signup_canvas, bg="white")
    signup_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    title = Label(signup_frame, text="SignUp to continue", fg="foreground_black", bg="white")
    title.config(font='calibri 40')
    title.place(relx=0.2, rely=0.1)

    # full name
    name_label = Label(signup_frame, text="Name:", fg='foreground_black', bg='white')
    name_label.place(relx=0.21, rely=0.4)
    name_entry = Entry(signup_frame, bg='#252526', fg='white', textvariable=name_entry, relief=FLAT)
    name_entry.config(width=42)
    name_entry.place(relx=0.31, rely=0.4)

    # username
    username_label = Label(signup_frame, text="Username: ", fg='foreground_black', bg='white')
    username_label.place(relx=0.21, rely=0.5)
    username_entry = Entry(signup_frame, bg='foreground_black', fg='white', textvariable=username, relief=FLAT)
    username_entry.config(width=42)
    username_entry.place(relx=0.31, rely=0.5)

    # password
    password_label = Label(signup_frame, text="Password: ", fg='foreground_black', bg='white')
    password_label.place(relx=0.215, rely=0.6)
    password_entry = Entry(signup_frame, bg='foreground_black', fg='white', textvariable=password, show="*", relief=FLAT)
    password_entry.config(width=42)
    password_entry.place(relx=0.31, rely=0.6)

    # country
    country_label = Label(signup_frame, text="Country: ", fg='foreground_black', bg='white')
    country_label.place(relx=0.217, rely=0.7)
    country_entry = Entry(signup_frame, bg='foreground_black', fg='white', textvariable=country, relief=FLAT)
    country_entry.config(width=42)
    country_entry.place(relx=0.31, rely=0.7)

    def addUserToDataBase():

        fullname = name_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        country = country_entry.get()

        if len(name_entry.get()) == 0 and len(username_entry.get()) == 0 and len(password_entry.get()) == 0 \
                and len(country_entry.get()) == 0:
            error = Label(text="Please enter all fields", fg='foreground_black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(name_entry.get()) == 0 or len(username_entry.get()) == 0 or len(password_entry.get()) == 0 \
                or len(country_entry.get()) == 0:
            error = Label(text="Please Enter all the fields", fg='foreground_black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(username_entry.get()) == 0 and len(password_entry.get()) == 0:
            error = Label(text="Username and password can't be empty", fg='foreground_black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(username_entry.get()) == 0 and len(password_entry.get()) != 0:
            error = Label(text="Username can't be empty", fg='foreground_black', bg='white')
            error.place(relx=0.37, rely=0.7)

        elif len(username_entry.get()) != 0 and len(password_entry.get()) == 0:
            error = Label(text="Password can't be empty", fg='foreground_black', bg='white')
            error.place(relx=0.37, rely=0.7)

        else:

            connect = sqlite3.connect('quiz.db')
            create = connect.cursor()
            create.execute(
                'CREATE TABLE IF NOT EXISTS userSignUp(FULLNAME text, USERNAME text,PASSWORD text,COUNTRY text)')
            create.execute("INSERT INTO userSignUp VALUES (?,?,?,?)", (fullname, username, password, country))
            connect.commit()
            create.execute('SELECT * FROM userSignUp')
            fetch_all = create.fetchall()
            print(fetch_all)
            connect.close()
            loginPage(fetch_all)

    def gotoLogin():
        conn = sqlite3.connect('quiz.db')
        create = conn.cursor()
        conn.commit()
        create.execute('SELECT * FROM userSignUp')
        z = create.fetchall()
        loginPage(z)

    # signup BUTTON
    sp = Button(signup_frame, text='SignUp', padx=5, pady=5, width=5, command=addUserToDataBase, bg="foreground_black", fg="white")
    sp.configure(width=15, height=1, activebackground="#33B5E5", relief=FLAT)
    sp.place(relx=0.4, rely=0.8)

    log = Button(signup_frame, text='Already have a Account?', padx=5, pady=5, width=5, command=gotoLogin, bg="white",
                 fg="foreground_black")
    log.configure(width=16, height=1, activebackground="white", relief=FLAT)
    log.place(relx=0.393, rely=0.9)

    signup_page.mainloop()


def menu(parameter):
    login_window.destroy()
    global menu

    menu = Tk()
    menu.title('Quiz App Menu')
    menu.resizable(False, False)

    menu_canvas = Canvas(menu, width=720, height=440, bg="orange")
    menu_canvas.pack()

    img = PhotoImage(file="nature.png")
    menu_canvas.create_image(2, 1, image=img, anchor=NW)

    menu_frame = Frame(menu_canvas, bg="white")
    menu_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    wel = Label(menu_canvas, text='Welcome to the quiz app by Amey', fg="white", bg='foreground_black')
    wel.config(font='verdana 25')
    wel.place(relx=0.1, rely=0.02)

    parameter = 'Welcome ' + parameter
    level34 = Label(menu_frame, text=parameter, bg="white", font="calibri 18", fg="white")
    level34.place(relx=0.17, rely=0.15)

    level = Label(menu_frame, text='Select your Difficulty Level:', bg="white", fg='foreground_black', font="calibri 18")
    level.place(relx=0.25, rely=0.3)

    variable = IntVar()
    easy_radiobutton = Radiobutton(menu_frame, text='Easy', bg="white", font="calibri 16", value=1, variable=variable)
    easy_radiobutton.place(relx=0.25, rely=0.4)

    medium_radiobutton = Radiobutton(menu_frame, text='Medium', bg="white", font="calibri 16", value=2,
                                     variable=variable)
    medium_radiobutton.place(relx=0.25, rely=0.5)

    hard_radiobutton = Radiobutton(menu_frame, text='Hard', bg="white", font="calibri 16", value=3, variable=variable)
    hard_radiobutton.place(relx=0.25, rely=0.6)

    def navigate():

        x = variable.get()
        print(x)
        if x == 1:
            menu.destroy()
            easy()
        elif x == 2:
            menu.destroy()
            medium()

        elif x == 3:
            menu.destroy()
            difficult()
        else:
            pass

    continue_button = Button(menu_frame, text="Let's Go", bg="foreground_black", fg="white", font="calibri 12", command=navigate)
    continue_button.place(relx=0.25, rely=0.8)
    menu.mainloop()


def easy():
    global easy_window
    easy_window = Tk()
    easy_window.title('Quiz App - Easy Level')
    easy_window.resizable(False, False)

    easy_canvas = Canvas(easy_window, width=720, height=440, bg="orange")
    easy_canvas.pack()

    image = PhotoImage(file="tree.png")
    easy_canvas.create_image(2, 1, image=image, anchor=NW)

    easy_frame = Frame(easy_canvas, bg="white")
    easy_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(10, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            easy_frame.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0

    easy_questions = [
        [
            "What is the capital of Japan?",
            "Tokyo",
            "Seoul",
            "Stockholm",
            "Shanghai"
        ],
        [
            "Which of these animals are NOT extinct?",
            "Dodo",
            "White Rhinoceros",
            "Mammoth",
            "Great Auk"

        ],
        [
            "Which of these are one of the  NEW seven wonders of the world?",
            "The hanging gardens of Babylon",
            "The lighthouse of Alexandria",
            "The statue of Liberty",
            "None of these"
        ],
        [
            "How many moons does Neptune have?",
            "14",
            "35",
            "46",
            "8"
        ],
        [
            "When you combine yellow and blue, what do you get?",
            "Indigo",
            "Green",
            "Violet",
            "Light Blue"
        ]
    ]
    answer = [
        "Tokyo",
        "White Rhinoceros",
        "The statue of Liberty",
        "14",
        "Green"
    ]
    list = ['', 0, 1, 2, 3, 4]
    x = random.choice(list[1:])

    ques = Label(easy_frame, text=easy_questions[x][0], font="calibri 12", bg="white", fg='#33b1ff')
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    variable = StringVar()

    a = Radiobutton(easy_frame, text=easy_questions[x][1], font="calibri 10", value=easy_questions[x][1],
                    variable=variable, bg="white", fg='#e91e07')
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(easy_frame, text=easy_questions[x][2], font="calibri 10", value=easy_questions[x][2],
                    variable=variable, bg="white", fg='#e91e07')
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(easy_frame, text=easy_questions[x][3], font="calibri 10", value=easy_questions[x][3],
                    variable=variable, bg="white", fg='#e91e07')
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(easy_frame, text=easy_questions[x][4], font="calibri 10", value=easy_questions[x][4],
                    variable=variable, bg="white", fg='#e91e07')
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    list.remove(x)

    timer = Label(easy_window)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():

        if len(list) == 1:
            easy_window.destroy()
            marks(score)
        if len(list) == 2:
            next_button.configure(text='End', command=calc)

        if list:
            x = random.choice(list[1:])
            ques.configure(text=easy_questions[x][0])

            a.configure(text=easy_questions[x][1], value=easy_questions[x][1])

            b.configure(text=easy_questions[x][2], value=easy_questions[x][2])

            c.configure(text=easy_questions[x][3], value=easy_questions[x][3])

            d.configure(text=easy_questions[x][4], value=easy_questions[x][4])

            list.remove(x)
            y = countDown()
            if y == -1:
                display()

    def calc():
        global score
        if (variable.get() in answer):
            score += 1
        display()

    submit = Button(easy_frame, command=calc, text="Submit", fg="white", bg="foreground_black")
    submit.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_button = Button(easy_frame, command=display, text="Next", fg="white", bg="foreground_black")
    next_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
    easy_window.mainloop()


def medium():
    global normal
    normal = Tk()
    normal.title('Quiz App - Medium Level')
    normal.resizable(False, False)

    normal_canvas = Canvas(normal, width=720, height=440)
    normal_canvas.pack()

    image = PhotoImage(file="sun.png")
    normal_canvas.create_image(2, 1, image=image, anchor=NW)

    normal_frame = Frame(normal_canvas, bg="white")
    normal_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(10, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            normal_frame.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0

    normal_questions = [
        [
            "Which of these are not a body of the Solar System?",
            "Lo",
            "Eris",
            "Titania",
            "Barnard-b"
        ],
        [
            "What is the capital of Denmark?",
            "Stockholm",
            "Helsinki",
            "Copenhagen",
            "Oslo"
        ],
        [
            "Which of these are not a programming language?",
            "C#",
            "AppleScript",
            "AndroidScript",
            "Ruby"
        ],
        [
            "Which of these are not a car brand?",
            "Ferrari",
            "Lamborghini",
            "Premium",
            "Kia"
        ],
        [
            "Which of these are not a type of plants?",
            "Creeper",
            "Runner",
            "Digger",
            "Tree"
        ],
    ]
    answer = [
        "Barnard-b",
        "Copenhagen",
        "AndroidScript",
        "Premium",
        "Digger"
    ]

    list = ['', 0, 1, 2, 3, 4]
    x = random.choice(list[1:])

    question_label = Label(normal_frame, text=normal_questions[x][0], font="calibri 14", bg="white", fg='#e31c1c')
    question_label.place(relx=0.5, rely=0.2, anchor=CENTER)

    variable = StringVar()

    a = Radiobutton(normal_frame, text=normal_questions[x][1], font="calibri 12", value=normal_questions[x][1],
                    variable=variable, bg="white", fg='#0aaef5')
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(normal_frame, text=normal_questions[x][2], font="calibri 12", value=normal_questions[x][2],
                    variable=variable, bg="white", fg='#0aaef5')
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(normal_frame, text=normal_questions[x][3], font="calibri 12", value=normal_questions[x][3],
                    variable=variable, bg="white", fg='#0aaef5')
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(normal_frame, text=normal_questions[x][4], font="calibri 12", value=normal_questions[x][4],
                    variable=variable, bg="white", fg='#0aaef5')
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    list.remove(x)

    timer = Label(normal)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():

        if len(list) == 1:
            normal.destroy()
            marks(score)
        if len(list) == 2:
            next_button.configure(text='End', command=calc)

        if list:
            x = random.choice(list[1:])
            question_label.configure(text=normal_questions[x][0])

            a.configure(text=normal_questions[x][1], value=normal_questions[x][1])

            b.configure(text=normal_questions[x][2], value=normal_questions[x][2])

            c.configure(text=normal_questions[x][3], value=normal_questions[x][3])

            d.configure(text=normal_questions[x][4], value=normal_questions[x][4])

            list.remove(x)
            y = countDown()
            if y == -1:
                display()

    def calc():
        global score
        if variable.get() in answer:
            score += 1
        display()

    submit = Button(normal_frame, command=calc, text="Submit", fg="white", bg="foreground_black")
    submit.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_button = Button(normal_frame, command=display, text="Next", fg="white", bg="foreground_black")
    next_button.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
    normal.mainloop()


def difficult():
    global hard

    hard = Tk()
    hard.title('Quiz App - Hard Level')

    hard_canvas = Canvas(hard, width=720, height=440, bg="#101357")
    hard_canvas.pack()

    image = PhotoImage(file="tree.png")
    hard_canvas.create_image(2, 1, image=image, anchor=NW)

    hard_frame = Frame(hard_canvas, bg="white")
    hard_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    def countDown():
        check = 0
        for k in range(10, 0, -1):

            if k == 1:
                check = -1
            timer.configure(text=k)
            hard_frame.update()
            time.sleep(1)

        timer.configure(text="Times up!")
        if check == -1:
            return -1
        else:
            return 0

    global score
    score = 0

    hard_questions = [
        [
            "What were the instruments used by the Egyptians to measure time except sundials?",
            "water clock",
            "wind clock",
            "Phases of the Moon",
            "None of these"
        ],
        [
            "What is the capital of Austria?",
            "Berlin",
            "Prague",
            "Budapest",
            "Vienna"
        ],
        [
            "Which of the following country's have the highest HDI rank?",
            "Finland",
            "Denmark",
            "Ireland",
            "Sweden"
        ],
        [
            "According to Greek Mythology, who is the king of gods?",
            "Zeus",
            "Prometheus",
            "Hercules",
            "None of these"
        ],
        [
            "Which of these are not the moons of Jupiter?",
            "Ganymede",
            "Lo",
            "Titan",
            "Callisto"
        ]

    ]
    answer = [
        "Water clock",
        "Vienna",
        "Ireland",
        "Zeus",
        "Callisto"
    ]

    list = ['', 0, 1, 2, 3, 4]
    x = random.choice(list[1:])

    ques = Label(hard_frame, text=hard_questions[x][0], font="calibri 12", fg="#018bf4", bg='white')
    ques.place(relx=0.5, rely=0.2, anchor=CENTER)

    var = StringVar()

    a = Radiobutton(hard_frame, text=hard_questions[x][1], font="calibri 10", value=hard_questions[x][1],
                    variable=var, bg="white", fg="#f40126")
    a.place(relx=0.5, rely=0.42, anchor=CENTER)

    b = Radiobutton(hard_frame, text=hard_questions[x][2], font="calibri 10", value=hard_questions[x][2],
                    variable=var, bg="white", fg="#f40126")
    b.place(relx=0.5, rely=0.52, anchor=CENTER)

    c = Radiobutton(hard_frame, text=hard_questions[x][3], font="calibri 10", value=hard_questions[x][3],
                variable=var, bg="white", fg="#f40126")
    c.place(relx=0.5, rely=0.62, anchor=CENTER)

    d = Radiobutton(hard_frame, text=hard_questions[x][4], font="calibri 10", value=hard_questions[x][4],
                    variable=var, bg="white", fg="#f40126")
    d.place(relx=0.5, rely=0.72, anchor=CENTER)

    list.remove(x)

    timer = Label(hard)
    timer.place(relx=0.8, rely=0.82, anchor=CENTER)

    def display():

        if len(list) == 1:
            hard.destroy()
            marks(score)
        if len(list) == 2:
            next_question.configure(text='End', command=calc)

        if list:
            x = random.choice(list[1:])
            ques.configure(text=hard_questions[x][0])

            a.configure(text=hard_questions[x][1], value=hard_questions[x][1])

            b.configure(text=hard_questions[x][2], value=hard_questions[x][2])

            c.configure(text=hard_questions[x][3], value=hard_questions[x][3])

            d.configure(text=hard_questions[x][4], value=hard_questions[x][4])

            list.remove(x)
            y = countDown()
            if y == -1:
                display()

    def calc():
        global score
        # count=count+1
        if var.get() in answer:
            score += 1
        display()

    submit = Button(hard_frame, command=calc, text="Submit", fg="white", bg="foreground_black")
    submit.place(relx=0.5, rely=0.82, anchor=CENTER)

    next_question = Button(hard_frame, command=display, text="Next", fg="white", bg="foreground_black")
    next_question.place(relx=0.87, rely=0.82, anchor=CENTER)

    y = countDown()
    if y == -1:
        display()
    hard.mainloop()


def marks(mark):
    marks_window = Tk()
    marks_window.title('Your Marks')

    result = "Your score is " + str(mark) + "/5"
    result_label = Label(marks_window, text=result, fg="foreground_black", bg="white")
    result_label.pack()

    def callsignUpPage():
        marks_window.destroy()
        start()

    def myeasy():
        marks_window.destroy()
        easy()

    re_attempt_button = Button(text="Re-attempt", command=myeasy, bg="foreground_black", fg="white")
    re_attempt_button.pack()

    fig = Figure(figsize=(5, 4), dpi=100)
    labels = 'Marks Obtained', 'Total Marks'
    sizes = [int(mark), 5 - int(mark)]
    explode = (0.1, 0)
    fig.add_subplot(111).pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=0)

    canvas = FigureCanvasTkAgg(fig, master=marks_window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    sign_out_button = Button(text="Sign Out", command=callsignUpPage, fg="white", bg="foreground_black")
    sign_out_button.pack()

    marks_window.mainloop()


def start():
    global root
    root = Tk()
    root.title('Welcome To Quiz App')
    root.resizable(False, False)
    canvas = Canvas(root, width=720, height=440, bg='foreground_black')
    canvas.grid(column=0, row=1)
    img = PhotoImage(file="sun.png")
    canvas.create_image(2, 1, image=img, anchor=NW)

    button = Button(root, text='Start', command=signUpPage, bg="foreground_black", fg="yellow")
    button.configure(width=102, height=2, activebackground="#33B5E5", relief=RAISED)
    button.grid(column=0, row=2)

    root.mainloop()


if __name__ == '__main__':
    start()
