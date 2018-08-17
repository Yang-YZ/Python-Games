# Mini-project #6 - Blackjack

import random
import simplegui

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome_dealer = ""
outcome_player = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        """
        create Hand object
        """
        self.card_list = []

    def __str__(self):
        """
        return a string representation of a hand
        """
        hand_str = "Hand contains"
        for i in range(len(self.card_list)):
            hand_str += " " + self.card_list[i].suit + self.card_list[i].rank
        return hand_str

    def add_card(self, card):
        """
        add a card object to a hand
        """
        self.card_list.append(card)

    def get_value(self):
        """
        compute the value of the hand
        count aces as 1, if the hand has an ace, 
        then add 10 to hand value if it doesn't bust
        """
        hand_value = 0
        has_aces = False
        for card in self.card_list:
            hand_value += VALUES[card.rank]
            if card.rank == "A":
                has_aces = True        
        if has_aces == True:
            if (hand_value + 10) <= 21:
                hand_value += 10
        return hand_value
   
    def draw(self, canvas, pos):
        """
        draw a hand on the canvas, use the draw method for cards
        """
        for c in self.card_list:
            c.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]

        
# define deck class 
class Deck:
    def __init__(self):
        """create a Deck object
        """
        self.card_list = []
        for suit in SUITS:
            for rank in RANKS:
                # create a Card object using Card(suit, rank) and add it to the card list for the deck
                card = Card(suit, rank)
                self.card_list.append(card)
        
    def shuffle(self):
        """
        shuffle the deck
        """
        random.shuffle(self.card_list)
        return self.card_list

    def deal_card(self):
        """
        deal a card object from the deck
        """
        return self.card_list.pop()
    
    def __str__(self):
        """
        return a string representing the deck
        """
        hand_str = "Deck contains"
        for i in range(len(self.card_list)):
            hand_str += " " + self.card_list[i].suit + self.card_list[i].rank
        return hand_str


#define event handlers for buttons
def deal():
    global outcome_dealer, outcome_player, in_play, score, the_deck, player_hand, dealer_hand
    # if the "Deal" button is clicked during the middle of a round, 
    # player lost and updates the score appropriately.
    if in_play == True:
        outcome_dealer = "Player loses."
        score -= 1
    else:
        the_deck = Deck()
        the_deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(the_deck.deal_card())
        player_hand.add_card(the_deck.deal_card())
        dealer_hand.add_card(the_deck.deal_card())
        dealer_hand.add_card(the_deck.deal_card())
        outcome_dealer = ""
        outcome_player = "Hit or stand?"
        in_play = True    
    print "Dealer's "
    print dealer_hand
    print "Player's "
    print player_hand

def hit():
    global outcome_dealer, outcome_player, in_play, score, the_deck, player_hand, dealer_hand
    # if the hand is in play, hit the player
    if in_play == True:
        if player_hand.get_value() <= 21:
            player_hand.add_card(the_deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome_dealer = "Player has busted."
            outcome_player = "New deal?"
            in_play = False
            score -= 1
    print "Dealer's "
    print dealer_hand
    print "Player's "
    print player_hand

def stand():
    global outcome_dealer, outcome_player, in_play, score, the_deck, player_hand, dealer_hand
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(the_deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            outcome_dealer = "Dealer has busted."
            score += 1
        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome_dealer = "Dealer wins."
                score -= 1
            else:
                outcome_dealer = "Player wins."
                score += 1
        in_play = False
        outcome_player = "New deal?"
    print "Dealer's "
    print dealer_hand
    print "Player's "
    print player_hand    

# draw handler    
def draw(canvas):
    dealer_hand.draw(canvas, [50, 250])
    player_hand.draw(canvas, [50, 450])
    canvas.draw_text('Blackjack', [50, 100], 70, 'Black')
    canvas.draw_text('Score' , [400, 100], 40, 'Black')
    canvas.draw_text(str(score), [530, 100], 40, 'Black')
    canvas.draw_text('Dealer', [50, 200], 30, 'Gray')
    canvas.draw_text(outcome_dealer, [350, 200], 30, 'Yellow')
    canvas.draw_text('Player', [50, 400], 30, 'Gray')
    canvas.draw_text(outcome_player, [350, 400], 30, 'Yellow')        
    if in_play == True:
        card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0], CARD_BACK_CENTER[1] + CARD_BACK_SIZE[1])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 250 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
