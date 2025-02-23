from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"



# ---------------------------- SAVE PROGRESS ------------------------------- #

# ---------------------------- FLIP CARD ------------------------------- #

current_card = {}
to_learn = {}

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    
  

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_title, text="French", fill="white")
    canvas.itemconfig(canvas_word, text=current_card["French"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)
    flip_timer= window.after(5000, flip_card)

def flip_card():
    canvas.itemconfig(canvas_title, text="English", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)

def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data_save = pd.DataFrame(to_learn)
    data_save.to_csv("data/words_to_learn.csv", index=False)

    next_card()

# ---------------------------- GUI SETUP ------------------------------- #
window = Tk()
window.title("Flashy Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer= window.after(5000, flip_card)

#main canvas button
canvas = Canvas(width=800, height=526)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

canvas_title = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 260, font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

#unknown and check buttons
unknown_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image= unknown_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_image = PhotoImage(file="images/right.png")
known_button = Button(image= known_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
