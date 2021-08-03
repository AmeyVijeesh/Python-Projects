from tkinter import *
import time
from datetime import datetime
from apps import weather_app, on_screen_keyboard, calculator, web_browser, calendar_app, stopwatch

root = Tk()
root.geometry("366x650")
root.resizable(0, 0)
root.title("Phone Simulator")

image1 = PhotoImage(file='img.png')
canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=True)


def start():
    today = datetime.today()

    current_time = time.strftime("%I:%M %p")
    current_date = today.strftime("%B %d, %Y")
    current_day = today.strftime('%A')
    time_bar['text'] = f'{current_time} {current_date} {current_day}'
    time_bar.after(1, start)

def search():
    user_input = (find_entry.get()).upper()
    if user_input == 'CALCULATOR':
        calculator()

    elif user_input == 'KEYBOARD':
        on_screen_keyboard()

    elif user_input == 'WEATHER':
        weather_app()

    elif user_input == 'BROWSER':
        web_browser()

    elif user_input == 'CALENDAR':
        calendar_app()

    elif user_input == 'STOPWATCH':
        stopwatch()


canvas.create_image(0, 0, image=image1, anchor=NW)

time_bar = Label(root, font=('Arial', 15), bg='black', fg='white', width=39)
time_bar.place(x=5, y=3)

find_entry = Entry(canvas, width=20, font=('Arial', 15))
find_entry.place(x=50, y=150)

search_btn = Button(root, text='Search!', height=2, command=search)
search_btn.place(x=270, y=145)

app1 = Button(canvas, text='Weather', highlightbackground='grey', activeforeground='white', fg='black', width=7,
              height=2, command=weather_app)
app1.place(x=50, y=300)

app2 = Button(canvas, text='Keyboard', highlightbackground='grey', activeforeground='white', fg='black', width=7,
              height=2, command=on_screen_keyboard)
app2.place(x=150, y=300)

app3 = Button(canvas, text='Calculator', highlightbackground='grey', activeforeground='white', fg='black', width=7,
              height=2, command=calculator)
app3.place(x=250, y=300)

app4 = Button(canvas, text='Browser', highlightbackground='grey', activeforeground='white', fg='black', width=7,
              height=2, command=web_browser)
app4.place(x=50, y=400)

app5 = Button(canvas, text='Calendar', highlightbackground='grey', activeforeground='white', fg='black', width=7,
              height=2, command=calendar_app)
app5.place(x=150, y=400)

app6 = Button(canvas, text='StopWatch', highlightbackground='grey', activeforeground='white', fg='black', width=7,
              height=2, command=stopwatch)
app6.place(x=250, y=400)


start()
root.mainloop()
