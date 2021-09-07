
from tkinter import * # pip install python-tk
import requests # pip install requests
from PIL import Image, ImageTk # pip install Pillow
from io import BytesIO # No installation needed.

root = Tk()
root.title('Online Image Viewer - Open online Images!')
root.geometry('600x500') 

Label(root, text='', width=22, height=9).pack(side=TOP)

label = Label(root, bg='white')
label.pack(side='top')

var = StringVar()
entry = Entry(root, justify='center', textvariable=var)
entry.focus_set()
entry.place(x=200, y=40)

web_imgs = []


class WebImage:
    def __init__(self, url):
        u = requests.get(url)
        self.image = ImageTk.PhotoImage(Image.open(BytesIO(u.content)))

    def get(self):
        return self.image


def create_img():
    image = WebImage(entry.get())
    web_imgs.append(image)
    label.config(image=image.get())


go_btn = Button(root, text='Go', width=5, command=create_img)
go_btn.place(x=270, y=100)
root.mainloop()
