# Importing required libraries
from tkinter import *
import random
from tkinter import messagebox

# Setting up the interface
root = Tk()
root.geometry('522x200+400+100')
root.title('Typing Speed Tester by Amey')
root.resizable(False, False)
root.configure(bg="white")

# required variables
total_score = 0
time_left = 60
counting = 0
blank_words = ''
incorrect = 0

# List of words that will be asked to the user
words = ['interesting', 'excitement', 'fastest', 'slowest', 'remember', 'ordinary', 'memories', 'darkness',
         'absolute', 'account', 'argument', 'building', 'brother', 'efficiency', 'encouraged', 'typewriter',
         'percentage', 'performance', 'department', 'dependent', 'leadership', 'laboratory', 'networking',
         'navigator', 'category', 'challenge', 'recognized', 'reasonable', 'technology', 'transition', 'tournament',
         'scientific', 'statements', 'strategies', 'zigzagging', 'yourselves', 'themselves', 'weaknesses'] # You can add more words. 
# The more the words, the more options for the player.


def labelMarquee():
    global counting
    global blank_words
    text = 'Welcome to Typing speed tester by Amey'
    if counting >= len(text):
        counting = 0
        blank_words = ''
    blank_words += text[counting]
    counting += 1
    title.configure(text=blank_words)
    title.after(200, labelMarquee)


def time():
    global time_left, total_score, incorrect
    if time_left > 0:
        time_left -= 1
        time_count.configure(text=time_left)
        time_count.after(1000, time)
    else:
        score_count.configure(text=(total_score - incorrect))
        instruction.configure(
            text='Correct: {} | Incorrect: {} | Total: {}'.format(
                total_score, incorrect, (total_score - incorrect)))
        ask = messagebox.askretrycancel('Play Again', 'Do you want to play again?')
        if ask > 0:
            total_score = 0
            time_left = 60
            incorrect = 0
            time_count.configure(text=time_left)
            words_label.configure(text=words[0])


def startGame(event):
    global total_score
    global incorrect
    if time_left == 60:
        time()
    instruction.configure(text='')

    if words_entry.get() == words_label['text']:
        total_score += 1
    else:
        incorrect += 1

    random.shuffle(words)
    words_label.configure(text=words[0])
    words_entry.delete(0, END)
    score_count.configure(text=total_score)


title = Label(root, text='', font=('open sans', 16, 'bold'), width=39, bg='white', fg="gold")
title.place(x=5, y=5)
labelMarquee()

timer_label = Label(root, text='Time Left', font=('verdana', 15, 'bold'), bg='white', fg='black')
timer_label.place(x=400, y=45)
time_count = Label(root, text=time_left, font=('verdana', 12, 'bold'), bg='white', fg='red')
time_count.place(x=445, y=80)

score = Label(root, text='Your Score', font=('verdana', 15, 'bold'), bg='white', fg='green')
score.place(x=10, y=45)
score_count = Label(root, text=total_score, font=('verdana', 12, 'bold'), bg='white', fg='blue')
score_count.place(x=60, y=80)

random.shuffle(words)
words_label = Label(root, text=words[0], font=('sans serif', 18, 'bold'), width=20, fg='silver', bg='white')
words_label.place(x=105, y=100)

instructions = Label(root, text='Type the above word as fast as you can!', font=('verdana', 10, 'underline', 'bold'),
                    bg='white', fg='brown')
instructions.place(x=115, y=172)

words_entry = Entry(root, font=('calibri bold', 16), relief=FLAT, justify='center', width=35, bg='white',
                    fg='light blue')
words_entry.place(x=60, y=140)
words_entry.focus_set()

root.bind('<Return>', startGame)
root.mainloop()
