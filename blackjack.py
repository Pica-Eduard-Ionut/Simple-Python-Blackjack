import random
import tkinter as tk
from PIL import Image, ImageTk

def enable_buttons(bool):
    if bool == False:
        dealer_button.config(state="disabled")
        player_button.config(state="disabled")
        shuffle_button.config(state="disabled")
    elif bool == True:
        dealer_button.config(state="normal")
        player_button.config(state="normal")
        shuffle_button.config(state="normal")

def load_images(card_images):
    for card in range(2, 15):
        name = f"images/{card}.png"
        image = Image.open(name)
        photo = ImageTk.PhotoImage(image)
        card_images.append((card, photo))

def _deal_card(frame):
    next_card = deck.pop(0)
    deck.append(next_card)
    tk.Label(frame, image=next_card[1], relief="raised").pack(side="left")
    return next_card

def score_hand(hand):
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 14 and not ace:
            ace = True
            card_value = 11
        elif card_value > 10 and card_value < 14:
            card_value = 10
        score += card_value

        # if we would bust, check if there is an ace and subtract 10
        if score > 21 and ace:
            score -= 10
            ace = False
    return score

def deal_dealer():
    dealer_score = score_hand(dealer_hand)
    global count

    while 0 < dealer_score < 17:
        dealer_hand.append(_deal_card(dealer_card_frame))
        dealer_score = score_hand(dealer_hand)
        dealer_score_label.set(dealer_score)

    player_score = score_hand(player_hand)
    if player_score > 21:
        result_text.set("Dealer wins!")
        enable_buttons(False)
        count = 0
        winstreak_text.set("Current winstreak: "+str(count))
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
        count += 1
        enable_buttons(False)
        winstreak_text.set("Current winstreak: "+str(count))
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
        count = 0
        winstreak_text.set("Current winstreak: "+str(count))
        enable_buttons(False)
    else:
        result_text.set("Draw!")
        enable_buttons(False)

def deal_player():
    global count

    player_score = score_hand(player_hand)
    if player_score < 21:  # Check if player's score is less than or equal to 21
        player_hand.append(_deal_card(player_card_frame))
        player_score = score_hand(player_hand)
        player_score_label.set(player_score)
    if player_score > 21:
        result_text.set("Dealer Wins!")
        enable_buttons(False)
        count = 0
        winstreak_text.set("Current winstreak: "+str(count))
    if player_score == 21:
        enable_buttons(False)
        deal_dealer()


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()
    if score_hand(player_hand) > 21:
        enable_buttons(False)
        new_game()
    elif score_hand(player_hand) == 21:
        enable_buttons(False)
        deal_dealer()

def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand

    enable_buttons(True)
    
    dealer_card_frame.destroy()
    dealer_card_frame = tk.Frame(card_frame, bg="green")
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

    player_card_frame.destroy()
    player_card_frame = tk.Frame(card_frame, bg="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")

    dealer_hand = []
    player_hand = []
    initial_deal()
    if score_hand(player_hand) > 21: # never start games with losing hands
        new_game()

def shuffle():
    random.shuffle(deck)

def play():
    initial_deal()
    mainWindow.mainloop()

mainWindow = tk.Tk()

# Set up the screen and frames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("800x350")
mainWindow.configure(bg="green")

mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=2)
mainWindow.columnconfigure(2, weight=2)
mainWindow.columnconfigure(3, weight=0)
mainWindow.columnconfigure(4, weight=5)
mainWindow.columnconfigure(5, weight=0)

result_text = tk.StringVar()
result = tk.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tk.Frame(mainWindow, relief="sunken", borderwidth=1, bg="black")
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)

dealer_score_label = tk.IntVar()
tk.Label(card_frame, text="Dealer", bg="black", fg="white").grid(row=0, column=0)
tk.Label(card_frame, textvariable=dealer_score_label, bg="black", fg="white").grid(row=1, column=0)
dealer_card_frame = tk.Frame(card_frame, bg="black")
dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

player_score_label = tk.IntVar()
tk.Label(card_frame, text="Player", bg="black", fg="white").grid(row=2, column=0)
tk.Label(card_frame, textvariable=player_score_label, bg="black", fg="white").grid(row=3, column=0)
player_card_frame = tk.Frame(card_frame, bg="black")
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

button_frame = tk.Frame(mainWindow)
button_frame.grid(row=3, column=1, columnspan=3, sticky='w')

player_button = tk.Button(button_frame, text="Hit", command=deal_player, padx=8)
player_button.grid(row=0, column=0)

dealer_button = tk.Button(button_frame, text="Stay", command=deal_dealer, padx=5)
dealer_button.grid(row=0, column=1)

reset_button = tk.Button(button_frame, text="New Game", command=new_game)
reset_button.grid(row=0, column=2)

shuffle_button = tk.Button(button_frame, text="Shuffle", command=shuffle, padx=2)
shuffle_button.grid(row=0, column=3)

global count
count = 0
winstreak_text = tk.IntVar()
winstreak = tk.Label(mainWindow, textvariable=winstreak_text)
winstreak.grid(row=4, column=0, columnspan=3)
winstreak_text.set("Current winstreak: "+str(count))

# Load card images
cards = []
load_images(cards)

# Create a new deck of cards and shuffle them
deck = list(cards) * 3  # Three decks of cards
shuffle()

# Create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()
