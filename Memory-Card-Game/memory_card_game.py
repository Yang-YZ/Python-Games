"""
implementation of card game - Memory
"""

import random
import simplegui

def new_game():
	"""
	helper function to initialize globals
	"""
    global state, counter, exposed, cards
    state = 0
    counter = 0
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    # creat a list with 16 numbers
    cards = range(8)
    cards.extend(cards)
    random.shuffle(cards)

def mouse_click(pos):
    """
	define event handlers
	"""
    global state, counter, card_index0, card_index1
    counter += 1
    label.set_text("Turns = " + str(counter))
    exposed[pos[0] // 50] = True
    if state == 0:
        state = 1
        card_index0 = pos[0] // 50      
    elif state == 1:
        state = 2
        card_index1 = pos[0] // 50
    else:
        if cards[card_index0] != cards[card_index1]:
            exposed[card_index0] = False
            exposed[card_index1] = False
        state = 1
        card_index0 = pos[0] // 50
 
def draw(canvas):
	"""
	draw the canvas
	"""
	# cards are logically 50x100 pixels in size
    for index in range(len(cards)):
        if exposed[index] == True:
            canvas.draw_text(str(cards[index]), [50//2 + index * 50, 100//2 ], 30, "White")
        else:
            canvas.draw_polygon([(0 + index * 50, 0), (50 + index * 50, 0), (50 + index * 50, 100), (0 + index * 50, 100)], 5, 'Green', 'Green')        


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouse_click)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
