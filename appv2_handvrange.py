import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random
from statistics import mean

deck = [rank + suit for rank in "23456789TJQKA" for suit in "♠♥♦♣"]
suits = "♠♥♦♣"

def win_rank(hole_cards, com_cards):
    rank_array = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    straight_flush = False
    flush = False
    straight = False
    three_of_a_kind = False
    global win_type
    global win_high
    win_type = 0
    win_high = 0
    
    # Count the occurrence of each suit in community cards
    suit_count = {suit: sum(1 for card in com_cards if card[1] == suit) for suit in "♠♥♦♣"}
    
    # Determine the most frequent suit
    max_suit = max(suit_count, key=suit_count.get)
    max_suit_count = suit_count[max_suit]
    
    # Checking for royal/straight flushes and normal flushes
    if max_suit_count >= 3:
        com_suited_cards = [card for card in com_cards if card[1] == max_suit]
        hole_suited_cards = [card for card in hole_cards if card[1] == max_suit]

        hole_com_suited_unq = ([10 if x == "T" else x for x in {num[0] for num in 
                                                                            dict.fromkeys(hole_suited_cards + com_suited_cards)}])

        # Obtaining the cards of the same suit
        c=0
        for num in hole_com_suited_unq:
            try:                  
                hole_com_suited_unq[c] = int(num)
            except:
                hole_com_suited_unq[c] = rank_array.index(num) + 2
            c+=1
        hole_com_suited_unq = sorted(hole_com_suited_unq, reverse=True)

        # Checking for wheel straight flush
        wheel_set = [2,3,4,5,14]
        if len(hole_com_suited_unq) - 5 == len(set(hole_com_suited_unq) - set(wheel_set)):
            straight_flush = True
            high_card_for_straight_flush = 5

        # Checking for normal straight flush
        c=0
        while c<len(hole_com_suited_unq) - 4:
            if sum(hole_com_suited_unq[c:c+5]) == 5*(hole_com_suited_unq[c]-2):
                straight_flush = True
                high_card_for_straight_flush = rank_array[hole_com_suited_unq[c]-2]
                break
            c+=1

        # Outputting royal/straight flush if achieved
        if straight_flush == True:
            if high_card_for_straight_flush == "A":
                royal_flush = True
                win_type = 1
                return
            else:
                straight_flush = True
                win_type = 2
                win_high = rank_array.index(str(high_card_for_straight_flush))
                return
        else:
            # If Royal/Straight flush missed then flush possibility is left
            if len(hole_com_suited_unq) >= 5:
                flush = True

    # Checking for non-suit draws (four of a kind, full house, straights, three of a kind, one/two pair, high cards)
    count_map = {"2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, 
                "T": 0, "J": 0, "Q": 0, "K": 0, "A": 0}

    # Count the occurence of each card from community cards
    for card in com_cards:
        count_map[card[0]] += 1
    
    # Count the occurence of each cards in hole_cards:
    for card in hole_cards:
        count_map[card[0]] += 1
    
    # Checking for the number of times card was repeated
    max_num = None
    max_repeat = -1

    # Finding the most repeated cards and the number of times they were repeated
    for key, value in count_map.items():
        if value > max_repeat:
            max_repeat = value
            max_num = key
        # Accounting for high cards
        elif value == max_repeat:
            if rank_array.index(key) > rank_array.index(max_num):
                max_num = key

    # Checking for four of kind
    if max_repeat == 4:
        four_of_a_kind = True
        win_type = 3
        non_rep_cards = []
        for key, value in count_map.items():
            if value != 4 and value != 0:
                non_rep_cards.append(rank_array.index(key))
        win_high = rank_array.index(max_num)+(max(non_rep_cards)*0.01)
        return

    # Checking for straights (this is being checked first as it clashes with three of a kind condition)
    hole_com_unq = ([10 if x == "T" else x for x in {num[0] for num in 
                                                                    dict.fromkeys(hole_cards + com_cards)}])
    c=0
    for num in hole_com_unq:
        try:                  
            hole_com_unq[c] = int(num)
        except:
            hole_com_unq[c] = rank_array.index(num) + 2
        c+=1
    
    hole_com_unq = sorted(hole_com_unq, reverse=True)

    wheel_set = [2,3,4,5,14]
    if len(hole_com_unq) - 5 == len(set(hole_com_unq) - set(wheel_set)):
        straight = True
        high_card_for_straight = 5
    
    c=0
    while c<len(hole_com_unq) - 4:
        if sum(hole_com_unq[c:c+5]) == 5*(hole_com_unq[c]-2):
            straight = True
            high_card_for_straight = rank_array[hole_com_unq[c]-2]
            break
        c+=1
    
    # Checking for full houses and three of a kind
    if max_repeat == 3:
        # Array storing all the values repeated twice
        repeat2 = []
        for key, value in count_map.items():
            if value == 2:
                repeat2.append(key)
        
        # Array storing all the values repeated thrice 
        repeat3 = []
        for key, value in count_map.items():
            if value == 3:
                repeat3.append(key)

        # Full house and three of kind conditions
        if len(repeat3) == 2:
            if rank_array.index(repeat3[0]) > rank_array.index(repeat3[1]):
                full_house = True
                win_type = 4
                win_high = 3*rank_array.index(repeat3[0]) + 2*(rank_array.index(repeat3[1]))
                return
            else:
                full_house = True
                win_type = 4
                win_high = 3*(rank_array.index(repeat3[1])) + 2*(rank_array.index(repeat3[0]))
                return
        else:
            if len(repeat2) == 2:
                if rank_array.index(repeat2[0]) > rank_array.index(repeat2[1]):
                    full_house = True
                    win_type = 4
                    win_high = 3*(rank_array.index(repeat3[0])) + 2*(rank_array.index(repeat2[0]))
                    return
                else:
                    full_house = True
                    win_type = 4
                    win_high = 3*(rank_array.index(repeat3[0])) + 2*(rank_array.index(repeat2[1]))
                    return
            elif len(repeat2) == 1:
                full_house = True
                win_type = 4
                win_high = 3*(rank_array.index(repeat3[0])) + 2*(rank_array.index(repeat2[0]))
                return
            else:
                three_of_a_kind = True

    if flush == True:
        win_type = 5
        flush_set = [rank_array[x-2] for x in hole_com_suited_unq][:5]
        c=0
        for i in flush_set:
            if c == 0:
                win_high += rank_array.index(i)*20000
            elif c == 1:
                win_high += rank_array.index(i)*1000
            elif c == 2:
                win_high += rank_array.index(i)*50
            elif c == 3:
                win_high += rank_array.index(i)*2
            else:
                win_high += rank_array.index(i)*0.1
            c+=1
        return
    elif straight == True:
        win_type = 6
        win_high = rank_array.index(str(high_card_for_straight))
        return
    elif three_of_a_kind == True:
        win_type = 7
        non_rep_cards = []
        for key, value in count_map.items():
            if value == 1:
                non_rep_cards.append(rank_array.index(key))
        max1 = max(non_rep_cards)
        non_rep_cards.remove(max1)
        win_high = (rank_array.index(repeat3[0])*100) + max1 + (max(non_rep_cards)*0.01)
        return

    # Checking for one/two pair
    if max_repeat == 2:
        # Array storing all the values repeated twice 
        repeat2 = []
        for key, value in count_map.items():
            if value == 2:
                repeat2.append(key)

        non_rep_cards = []
        for key, value in count_map.items():
            if value == 1:
                non_rep_cards.append(rank_array.index(key))

        if len(repeat2) == 3:
            repeat2_dict = {key: rank_array.index(key) for key in repeat2}

            max_num = max(repeat2_dict, key=repeat2_dict.get)
            del repeat2_dict[max_num]
            max_num2 = max(repeat2_dict, key=repeat2_dict.get)

            two_pair = True
            win_type = 8

            non_rep_cards = []
            for key, value in count_map.items():
                if value == 1 or value == 2:
                    non_rep_cards.append(rank_array.index(key))

            non_rep_cards.remove(rank_array.index(max_num))
            non_rep_cards.remove(rank_array.index(max_num2))

            win_high = rank_array.index(max_num) + rank_array.index(max_num2) + (max(non_rep_cards)*0.01)
            return
        elif len(repeat2) == 2:
            if rank_array.index(repeat2[0]) > rank_array.index(repeat2[1]):
                two_pair = True
                win_type = 8
                win_high = rank_array.index(repeat2[0]) + rank_array.index(repeat2[1]) + (max(non_rep_cards)*0.01)
                return
            else:
                two_pair = True
                win_type = 8
                win_high = rank_array.index(repeat2[1]) + rank_array.index(repeat2[0]) + (max(non_rep_cards)*0.01)
                return
        else:
            one_pair = True
            win_type = 9
            max1 = max(non_rep_cards)
            non_rep_cards.remove(max1)
            max2 = max(non_rep_cards)
            non_rep_cards.remove(max2)
            max3 = max(non_rep_cards)
            non_rep_cards.remove(max3)
            win_high = (rank_array.index(repeat2[0])*1000) + (max1*50) + max2 + (max3*0.01)
            return

    # Checking for high card
    else:
        hole_rank_dict = {num[0]: rank_array.index(num[0]) for num in hole_cards}
        com_rank_dict = {num[0]: rank_array.index(num[0]) for num in com_cards}
        hole_and_com_rank_dict = hole_rank_dict | com_rank_dict
        high_card_set = [key for key, value in sorted(hole_and_com_rank_dict.items(), key=lambda item: item[1])]
        high_card = True
        win_type = 10
        c = 0
        for i in high_card_set[2:][::-1]:
            if c == 0:
                win_high += rank_array.index(i)*20000
            elif c == 1:
                win_high += rank_array.index(i)*1000
            elif c == 2:
                win_high += rank_array.index(i)*50
            elif c == 3:
                win_high += rank_array.index(i)*2
            else:
                win_high += rank_array.index(i)*0.1
            c+=1
        return

def multi_way_equity(simul, player_card_set, community_cards, dead_cards):
    win_rates = []
    tie_rates = []

    for i in range(len(player_card_set)):
        win_rates.append(0)
        tie_rates.append(0)
    
    for i in range(simul):
        deck = [rank + suit for rank in "23456789TJQKA" for suit in "♠♥♦♣"]
        for cards in player_card_set:
            deck.remove(cards[0])
            deck.remove(cards[1])
        
        if len(dead_cards) > 0:
            for card in dead_cards:
                deck.remove(card)
        
        ## Create community cards

        # Pre=flop sim
        if len(community_cards)==0:
            com_cards = []
            for j in range(5):
                card = random.choice(deck)
                deck.remove(card)
                com_cards.append(card)
        # Flop sim
        elif len(community_cards)==3:
            com_cards = []
            com_cards = community_cards[:3]
            for i in community_cards[:3]:
                deck.remove(i)
            for j in range(2):
                card = random.choice(deck)
                deck.remove(card)
                com_cards.append(card)
        # Turn sim
        elif len(community_cards)==4:
            com_cards = []
            com_cards = community_cards[:4]
            for i in community_cards[:4]:
                deck.remove(i)
            card = random.choice(deck)
            deck.remove(card)
            com_cards.append(card)

        # Forming the win profile
        c=1
        player_profile = {}
        for cards in player_card_set:
            win_rank(cards, com_cards)
            player_profile[c] = str(win_type)+"&"+str(win_high)
            c+=1

        # Find the minimum value
        arr = [x[:x.index("&")] for x in player_profile.values()]
        min_value = str(min([int(i) for i in arr]))

        # Find all values with the minimum value
        player_won = {key: values for key, values in player_profile.items() if values[:values.index("&")] == min_value}

        # If there is one clear winner then declare them
        if len(player_won) == 1:
            win_rates[int(list(player_won.keys())[0])-1]+=1
        # Check to see overlap winners and decide between win and draw
        else:
            in_win_high = -1
            high_player_won = None
            player_ties = []
            for key, values in player_won.items():
                if float(values[values.index("&")+1:]) > in_win_high:
                    in_win_high = float(values[values.index("&")+1:])
                    high_player_won = key
                    player_ties.clear()
                elif float(values[values.index("&")+1:]) == in_win_high:
                    if high_player_won != None:
                        player_ties.append(high_player_won)
                    player_ties.append(key)
                    high_player_won = None
            
            if high_player_won != None:
                win_rates[int(high_player_won)-1]+=1
            else:
                for i in player_ties:
                    tie_rates[i-1]+=1

    

    global win_percent, tie_percent
    win_percent = round(((win_rates[0])/simul)*100, 3)
    tie_percent = round((tie_rates[0]/simul)*100, 3)

def hand_v_range(simul, player_1, x_inp, com_cards, dead_cards):
    player_1 = ['A♥', 'K♥']
    player_1_rem = []

    deck = [rank + suit for rank in "AKQJT98765432" for suit in "♠♥♦♣"]
    for i in player_1:
        deck.remove(i)

    for i in com_cards:
        deck.remove(i)

    player_2_range = []

    for i in x_inp:
        p2_num_1, p2_num_2, p2_suitedness = i[0], i[1], i[2]
        # Suited logic
        if p2_suitedness == "s":
            card_combo = []
            for j in deck:
                if j.startswith(p2_num_1):
                    if p2_num_2+j[1] in deck:
                        card_combo.append(j)
                        card_combo.append(p2_num_2+j[1])
                        player_2_range.append(card_combo)
                        card_combo = []
        # Offsuit logic
        else:
            card_combo = []
            for j in deck:
                if j.startswith(p2_num_1):
                    avail_suit = ["♠","♥","♦","♣"]
                    avail_suit.remove(j[1])
                    for k in avail_suit:
                        if p2_num_2+k in deck:
                            card_combo.append(j)
                            card_combo.append(p2_num_2+k)
                            player_2_range.append(card_combo)
                            card_combo = []

    seen = set()
    player_2_range_final = []

    for cards in player_2_range:
        if cards[0] not in seen:
            player_2_range_final.append(cards)
            seen.add(cards[0])

    win_percent_array = []
    tie_percent_array = []
    c=0
    for i in player_2_range_final:
        player_card_set = [player_1,i]
        multi_way_equity(simul, player_card_set, com_cards, dead_cards)
        win_percent_array.append(win_percent)
        tie_percent_array.append(tie_percent)
        c+=1
    win_equity = round(mean(win_percent_array),3)
    tie_equity = round(mean(tie_percent_array),3)
    global result
    result = f"Player:: win rate: {win_equity}%, tie percent: {tie_equity}%\n"

class PokerTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Poker Table")
        self.root.geometry("1000x700+0+0")
        self.root.resizable(False, False)
        self.selected_box = None
        self.box_contents = {}
        self.card_positions = {}
        self.card_images = {}

        self.load_card_images()
        self.create_widgets()

    def load_card_images(self):
        suits = ["♠", "♥", "♦", "♣"]
        ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        folder_path = "cards"

        for suit in suits:
            for rank in ranks:
                file_name = f"{rank}{suit}.png"
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    image = Image.open(file_path).resize((30, 45))
                    self.card_images[f"{rank}{suit}"] = ImageTk.PhotoImage(image)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=700, bg="green")
        self.canvas.pack()
        self.canvas.create_oval(50, 200, 750, 500, fill="brown")

        self.player_spots = []
        self.community_spots = []
        self.dead_card_spots = []
        self.selection_cards = {}

        self.card_width = 30
        self.card_height = 45

        community_x_start = 200
        for i in range(5):
            x = community_x_start + i * (self.card_width + 10)
            y = 320
            spot = tk.Label(self.root, bg="white", width=5, height=3, relief="solid", bd=2)
            spot.place(x=x, y=y)
            spot.bind("<Button-1>", self.select_box)
            self.community_spots.append(spot)

        player_positions = [(-490, -20)]
        center_x, center_y = 500, 350
        for dx, dy in player_positions:
            x = center_x + dx
            y = center_y + dy
            spot1 = tk.Label(self.root, bg="white", width=5, height=3, relief="solid", bd=2)
            spot2 = tk.Label(self.root, bg="white", width=5, height=3, relief="solid", bd=2)
            spot1.place(x=x, y=y)
            spot2.place(x=x+40, y=y)
            spot1.bind("<Button-1>", self.select_box)
            spot2.bind("<Button-1>", self.select_box)
            self.player_spots.append((spot1, spot2))

        self.range_buttons = {}
        ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        x_start = 412
        y_start = 200
        btn_width = 4
        btn_height = 1
        x_spacing = 33
        y_spacing = 25

        for i, r2 in enumerate(ranks):
            for j, r1 in enumerate(ranks):
                if i < j:
                    label = f"{r2}{r1}s"
                    base_color = "lightblue"
                elif i > j:
                    label = f"{r1}{r2}o"
                    base_color = "lightpink"
                else:
                    label = f"{r1}{r2}"
                    base_color = "lightgreen"

                btn = tk.Button(self.root, text=label, width=btn_width, height=btn_height, relief="raised", bg=base_color)
                btn.place(x=x_start + j * x_spacing, y=y_start + i * y_spacing)

                def toggle_button(b=btn, color=base_color):
                    current = b.config('relief')[-1]
                    if current == "sunken":
                        b.config(relief="raised", bg=color)
                    else:
                        b.config(relief="sunken", bg="gold")

                btn.config(command=toggle_button)
                self.range_buttons[label] = btn

        dead_x_start = 100
        dead_y_start = 600
        self.canvas.create_text(dead_x_start - 50, dead_y_start + 10, text="Dead Cards", font=("Arial", 12, "bold"), fill="white")
        for i in range(16):
            x = dead_x_start + i * (self.card_width + 10)
            y = dead_y_start
            spot = tk.Label(self.root, bg="white", width=5, height=3, relief="solid", bd=2)
            spot.place(x=x, y=y)
            spot.bind("<Button-1>", self.select_box)
            self.dead_card_spots.append(spot)

        self.selection_area = {}

        self.equity_button = tk.Button(self.root, text="Calculate Equity", command=self.calculate_equity)
        self.equity_button.place(x=850, y=650)

        self.new_hand = tk.Button(self.root, text="New Hand", command=self.reset_table)
        self.new_hand.place(x=850, y=600)

        x_start_diamonds = 0
        x_start_spades = 455
        x_start_clubs = 0
        x_start_hearts = 455
        y_diamonds_spades = 0
        y_clubs_hearts = 60

        ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        x_spacing = 35

        for i, rank in enumerate(ranks):
            for suit, x_start, y_start in [("♦", x_start_diamonds, y_diamonds_spades),
                                           ("♠", x_start_spades, y_diamonds_spades),
                                           ("♣", x_start_clubs, y_clubs_hearts),
                                           ("♥", x_start_hearts, y_clubs_hearts)]:
                card_key = f"{rank}{suit}"
                if card_key in self.card_images:
                    img_label = tk.Label(self.root, image=self.card_images[card_key], bg="white")
                    img_label.card_name = card_key
                    img_label.place(x=x_start + i * x_spacing, y=y_start)
                    img_label.bind("<Button-1>", self.move_card_to_spot)
                    self.selection_area[card_key] = img_label
                    self.card_positions[img_label] = (x_start + i * x_spacing, y_start)

        self.accuracy_label_high = tk.Label(self.root, text="High Accuracy (Very Slow)")
        self.accuracy_label_high.place(x=850, y=250)

        self.accuracy_slider = tk.Scale(self.root, from_=5, to=1, orient="vertical")
        self.accuracy_slider.set(3)
        self.accuracy_slider.place(x=910, y=270)

        self.accuracy_label_low = tk.Label(self.root, text="Low Accuracy (Very Fast)")
        self.accuracy_label_low.place(x=858, y=375)

        self.preset_ranges = {
    "Select a Range": [],

    # 6-Max
    "UTG (6-max)": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "AJs", "KQs", "AKo"],
    "MP (6-max)": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "AJs", "ATs", "KQs", "QJs", "AKo", "AQo"],
    "CO (6-max)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "AKs", "A5s", "A4s", 
                   "KQs", "QJs", "JTs", "T9s", "98s", "87s", "76s", "AKo", "AQo", "AJo"],
    "BTN (6-max)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "AKs", "A5s", "A4s", 
                    "A3s", "A2s", "KTs", "K9s", "QTs", "Q9s", "J9s", "T9s", "98s", "87s", "76s", "65s", "54s", "AKo", 
                    "AQo", "AJo", "KQo", "KJo"],
    "SB (6-max)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "AKs", "AQs", "AJs", 
                   "ATs", "A5s", "KQs", "KJs", "QJs", "QTs", "JTs", "T9s", "98s", "AKo", "AQo"],
    "BB (6-max vs Limp)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "A2s", "A3s", 
                           "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", 
                           "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q4s", "Q5s", "Q6s", "Q7s", "Q8s", 
                           "Q9s", "QTs", "QJs", "J6s", "J7s", "J8s", "J9s", "JTs", "T7s", "T8s", "T9s", "97s", "98s", 
                           "86s", "87s", "75s", "76s", "64s", "65s", "54s", "A2o", "A3o", "A4o", "A5o", "A6o", "A7o", 
                           "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "KTo", "KJo", "KQo", "Q9o", 
                           "QTo", "QJo", "J9o", "JTo", "T9o", "98o", "87o", "76o"],

    # 9-Max
    "UTG (9-max)": ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "AJs", "KQs", "AKo"],
    "UTG+1 (9-max)": ["AA", "KK", "QQ", "JJ", "TT", "99", "AKs", "AQs", "AJs", "KQs", "AKo", "AQo"],
    "MP1 (9-max)": ["AA", "KK", "QQ", "JJ", "TT", "99", "88", "AKs", "AQs", "AJs", "ATs", "KQs", "KJs", "AKo", "AQo"],
    "MP2 (9-max)": ["77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "KQs", "KJs", 
                    "QJs", "AKo", "AQo", "AJo"],
    "HJ (9-max)": ["66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "KQs", 
                   "KJs", "QJs", "JTs", "AKo", "AQo", "AJo"],
    "CO (9-max)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "AKs", "AQs", "A5s", 
                   "A4s", "A3s", "KTs", "QTs", "JTs", "T9s", "98s", "AKo", "AQo", "AJo", "KQo"],
    "BTN (9-max)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "A2s", "A3s", "A4s", 
                    "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", 
                    "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q6s", "Q7s", "Q8s", "Q9s", "QTs", "QJs", "J7s", "J8s", 
                    "J9s", "JTs", "T7s", "T8s", "T9s", "98s", "87s", "76s", "65s", "54s", "AKo", "AQo", "AJo", "KJo", "QTo"],
    "SB (9-max)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "A2s", "A3s", "A4s", 
                   "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", "K5s", "K6s", 
                   "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q6s", "Q7s", "Q8s", "Q9s", "QTs", "QJs", "J7s", "J8s", 
                   "J9s", "JTs", "T7s", "T8s", "T9s", "98s", "87s", "76s", "65s", "54s", "AKo", "AQo", "AJo", "KJo", "QJo"],
    "BB (9-max vs Limp)": ["22", "33", "44", "55", "66", "77", "88", "99", "TT", "JJ", "QQ", "KK", "AA", "A2s", "A3s", 
                           "A4s", "A5s", "A6s", "A7s", "A8s", "A9s", "ATs", "AJs", "AQs", "AKs", "K2s", "K3s", "K4s", 
                           "K5s", "K6s", "K7s", "K8s", "K9s", "KTs", "KJs", "KQs", "Q4s", "Q5s", "Q6s", "Q7s", "Q8s", 
                           "Q9s", "QTs", "QJs", "J6s", "J7s", "J8s", "J9s", "JTs", "T7s", "T8s", "T9s", "97s", "98s", 
                           "86s", "87s", "75s", "76s", "64s", "65s", "54s", "A2o", "A3o", "A4o", "A5o", "A6o", "A7o", 
                           "A8o", "A9o", "ATo", "AJo", "AQo", "AKo", "K7o", "K8o", "K9o", "KTo", "KJo", "KQo", "Q9o", 
                           "QTo", "QJo", "J9o", "JTo", "T9o", "98o", "87o", "76o"]
}

        self.range_var = tk.StringVar()
        self.range_var.set("Select a Range")
        self.range_dropdown = tk.OptionMenu(self.root, self.range_var, *self.preset_ranges.keys(), command=self.apply_preset_range)
        self.range_dropdown.place(x=412, y=170)  # adjust if needed

    def select_box(self, event):
        for box in self.community_spots + [p[0] for p in self.player_spots] + [p[1] for p in self.player_spots] + self.dead_card_spots:
            box.config(highlightthickness=0)

        self.selected_box = event.widget
        self.selected_box.config(highlightthickness=3, highlightbackground="purple")

        if self.selected_box in self.box_contents:
            img_label = self.box_contents.pop(self.selected_box)
            x, y = self.card_positions[img_label]
            img_label.place(x=x, y=y)

    def move_card_to_spot(self, event):
        if self.selected_box and self.selected_box not in self.box_contents:
            obj = event.widget
            box_x, box_y = self.selected_box.winfo_x(), self.selected_box.winfo_y()
            obj.place(x=box_x, y=box_y)
            self.box_contents[self.selected_box] = obj
        elif self.selected_box and self.selected_box in self.box_contents:
            img_label = self.box_contents.pop(self.selected_box)
            x, y = self.card_positions[img_label]
            img_label.place(x=x, y=y)

    def reset_range_buttons(self):
        for label, btn in self.range_buttons.items():
            current_bg = btn.cget("bg")
            # Determine base color by label
            if 's' in label:
                base_color = "lightblue"
            elif 'o' in label:
                base_color = "lightpink"
            else:
                base_color = "lightgreen"
            btn.config(relief="raised", bg=base_color)


    def reset_table(self):
        for box, img_label in list(self.box_contents.items()):
            x, y = self.card_positions[img_label]
            img_label.place(x=x, y=y)
        self.accuracy_slider.set(3)
        self.box_contents.clear()
        self.reset_range_buttons()

    def get_selected_hand_range(self):
        selected_hands = []
        for hand, btn in self.range_buttons.items():
            if btn.config('relief')[-1] == 'sunken':
                if 's' in hand or 'o' in hand:
                    selected_hands.append(hand)
                else:  # pair (e.g., 44)
                    selected_hands.append(f"{hand}o")
        return selected_hands

    def apply_preset_range(self, selection):
        # First reset everything
        self.reset_range_buttons()
        
        # Then apply selection
        for hand in self.preset_ranges.get(selection, []):
            btn = self.range_buttons.get(hand)
            if btn:
                btn.config(relief="sunken", bg="gold")

    def calculate_equity(self):
        player_hand = []
        for i, (spot1, spot2) in enumerate(self.player_spots):
            if spot1 in self.box_contents and spot2 in self.box_contents:
                player_hand.append([self.box_contents[spot1].card_name, self.box_contents[spot2].card_name])
            elif spot1 in self.box_contents or spot2 in self.box_contents:
                messagebox.showerror("Error", "Each player must have exactly two hole cards!")
                return

        community_cards = [self.box_contents[spot].card_name for spot in self.community_spots if spot in self.box_contents]

        if len(player_hand) < 1:
            messagebox.showerror("Error", "There must be at least 1 set of hole cards for simulation to occur")
            return

        if len(community_cards) == 1 or len(community_cards) == 2:
            messagebox.showerror("Error", "There must be at no/at least 3/4 community cards!")
            return

        dead_cards = [self.box_contents[spot].card_name for spot in self.dead_card_spots if spot in self.box_contents]

        player_2_selected_range = self.get_selected_hand_range()

        if len(player_2_selected_range) == 0:
            messagebox.showerror("Error", "There must be at aleast one set of card combos chosen from the range")
            return

        accuracy_level = self.accuracy_slider.get()

        if accuracy_level == 1:
            simul = 500
        elif accuracy_level == 2:
            simul = 2000
        elif accuracy_level == 3:
            simul = 5000
        elif accuracy_level == 4:
            simul = 10000
        elif accuracy_level == 5:
            simul = 25000
        
        hand_v_range(simul,player_hand,player_2_selected_range, community_cards, dead_cards)

        messagebox.showinfo("Poker Equity Calculation", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = PokerTableGUI(root)
    root.mainloop()
