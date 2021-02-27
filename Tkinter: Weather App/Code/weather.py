  
import tkinter as tk
import requests


def formatResponse(weather):
    try:
        name = weather['name']
        description = weather['weather'][0]['description']
        temp = weather['main']['temp']
        result = "City: %s \nConditions: %s \nTemperature (°F): %s" % (name, description, temp)
    except KeyError:
        result = "Please retry"

    return result


def getWeather(city):
    weather_key = 'c03eeb08b471c10ca8057b5078e9ca0a'
    url = "http://api.openweathermap.org/data/2.5/weather"
    parameters = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params=parameters)
    weather = response.json()

    label['text'] = formatResponse(weather)


HEIGHT = 500
WIDTH = 600

root = tk.Tk()
root.resizable(0, 0)
root.title("Weather app")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

backgroundImage = tk.PhotoImage(file='nature.png')
backgroundLabel = tk.Label(root, image=backgroundImage)
backgroundLabel.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relx=0, relheight=1, relwidth=0.65)

button = tk.Button(frame, text="Get Weather", font=40, command=lambda: getWeather(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lowerFrame = tk.Frame(root, bg='#80c1ff', bd=10)
lowerFrame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.5, anchor='n')

label = tk.Label(lowerFrame, font=('open sans', 20))
label.place(relwidth=1, relheight=1)

root.mainloop()
