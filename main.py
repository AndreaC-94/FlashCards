from tkinter import *
from tkinter import messagebox
import pandas as pd
import random as rd
BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
current_card = {}
to_learn = {}
try:
    words = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/spanish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = words.to_dict(orient="records")


def new_card():
    global timer, current_card
    window.after_cancel(timer)
    current_card = rd.choice(to_learn)
    canvas.itemconfig(image_id, image=front_card)
    canvas.itemconfig(language_id, text="Spanish", fill="black")
    canvas.itemconfig(word_id, text=current_card["Spanish"].title(), fill="black")
    timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(image_id, image=back_card)
    canvas.itemconfig(language_id, text="English | Italian", fill="white")
    canvas.itemconfig(word_id, text=f"{current_card['English'].title()}\n{current_card['Italian'].title()}",
                      fill="white")


def remove():
    to_learn.remove(current_card)
    pd.DataFrame(to_learn).to_csv("data/words_to_learn.csv", index=False)
    new_card()


def reverse():
    check = messagebox.askyesno(title="Reset Learning", message="By pressing yes, you will reset the learned word"
                                                                ".\nAre you sure you want to do it?")
    if check:
        global to_learn
        to_learn = pd.read_csv("data/spanish_words.csv").to_dict(orient="records")


# Window
window = Tk()
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
window.title("Flashy")
timer = window.after(3000, new_card)

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
image_id = canvas.create_image(400, 263, image=front_card)
language_id = canvas.create_text(400, 150, text="text", font=LANGUAGE_FONT)
word_id = canvas.create_text(400, 263, text="word", font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="images/wrong.png")
right_image = PhotoImage(file="images/right.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=new_card)
right_button = Button(image=right_image, highlightthickness=0, command=remove)
wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)
errase_button = Button(text="Delete", highlightthickness=0, command=reverse)
errase_button.grid(row=2, column=0)

new_card()
window.mainloop()
