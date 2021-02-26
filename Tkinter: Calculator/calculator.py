from tkinter import *

root = Tk()
root.geometry('305x333')
root.config(bg='black')
root.title("Calculator")
root.resizable(False, False)
icon = PhotoImage(file='cal.ico')
root.iconphoto(False, icon)

expression = ""


def press(num):
    global expression
    expression = expression + str(num)

    result.set(expression)


def get_result():
    try:
        global expression

        total = str(eval(expression))

        result.set(total)

        expression = ''

    except SyntaxError:
        result.set("Error")


def clear():
    global expression
    expression = ''
    result.set('')


def hover(widget, entrance_foreground, exit_fg, on_entrance, on_exit):
    widget.bind("<Enter>", func=lambda e: widget.config(
        bg=on_entrance,
        fg=entrance_foreground
    ))

    widget.bind("<Leave>", func=lambda e: widget.config(
        bg=on_exit,
        fg=exit_fg
    ))


result = StringVar()

entry = Entry(root, width=50, highlightcolor='black', highlightbackground='black', highlightthickness=4,
              font=('arial', 25), relief='sunken', textvariable=result)
entry.pack(ipadx=35, ipady=5)

button_1 = Button(root, text='1', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(1))
button_1.place(x=2, y=60)
hover(button_1, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_2 = Button(root, text='2', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(2))
hover(button_2, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_2.place(x=75, y=60)
button_3 = Button(root, text='3', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(3))
button_3.place(x=150, y=60)
hover(button_3, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_4 = Button(root, text='4', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(4))
button_4.place(x=1, y=128)
hover(button_4, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_5 = Button(root, text='5', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(5))
hover(button_5, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_5.place(x=75, y=128)
button_6 = Button(root, text='6', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(6))
button_6.place(x=150, y=128)
hover(button_6, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_7 = Button(root, text='7', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(7))
hover(button_7, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_7.place(x=1, y=195)
button_8 = Button(root, text='8', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(8))
button_8.place(x=75, y=195)
hover(button_8, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_9 = Button(root, text='9', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(9))
button_9.place(x=150, y=195)
hover(button_9, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
button_0 = Button(root, text='0', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                  relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press(0))
button_0.place(x=1, y=260)
hover(button_0, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
plus_button = Button(root, text='+', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                     relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press("+"))
plus_button.place(x=225, y=60)
hover(plus_button, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
minus_button = Button(root, text='-', highlightcolor='black', highlightbackground='black', highlightthickness=4,
                      width=6, relief=FLAT, default='active', font=('calibri', 14), height=2,
                      command=lambda: press("-"))
hover(minus_button, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
minus_button.place(x=225, y=128)
mul_button = Button(root, text='x', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                    relief=FLAT, default='active', font=('calibri', 14), height=2, command=lambda: press("*"))
mul_button.place(x=225, y=195)
hover(mul_button, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
div_button = Button(root, text='/', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                    relief=FLAT, default='active', font=('calibri', 14), height=2)
div_button.place(x=225, y=260)
hover(div_button, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')
cle_button = Button(root, text='C', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                    relief=FLAT, default='active', font=('calibri', 14), height=2, command=clear)
cle_button.place(x=75, y=260)
hover(cle_button, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')

res_button = Button(root, text='=', highlightcolor='black', highlightbackground='black', highlightthickness=4, width=6,
                    relief=FLAT, default='active', font=('calibri', 14), height=2, command=get_result)
res_button.place(x=150, y=260)
hover(res_button, entrance_foreground='white', exit_fg='black', on_entrance='black', on_exit='white')

root.mainloop()
