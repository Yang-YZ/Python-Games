"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    
    This function takes as input a tuple hand 
    that represents the die values in the given Yahtzee hand. 
    Since ordering of the die values in Yahtzee hands is unimportant, 
    tuples corresponding to Yahtzee hands will always be stored 
    in sorted order to guarantee that each tuple corresponds to a unique Yahtzee hand. 
    The function score(hand) computes a score for hand as the maximum of the possible values
    for each choice of box in the upper section of the Yahtzee scorecard.
    """
    scores = dict([])
    for dice in hand:
        if scores.has_key(dice):
            scores[dice] += dice
        else:
            scores[dice] = dice
    return max(scores.values())


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    
    This function computes the expected value of the scores for the possible Yahtzee hands
    that result from holding some dice and rolling the remaining free dice. 
    The dice being held are specified by the sorted tuple held_dice. 
    The number of sides and the number of dice that are free to be rolled 
    are specified by num_die_sides and num_free_dice, respectively. 
    You should use gen_all_sequences to compute all possible rolls for the dice being rolled.
    As an example, in a standard Yahtzee game using five dice, 
    the length of held_dice plus num_free_dice should always be five.
    """
    all_rolls = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    probability = (1.0 / num_die_sides) ** num_free_dice
    expected = 0.0
    for roll in all_rolls:
        max_score = score(roll+held_dice)
        expected += max_score
    expected *= probability
    return expected


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    
    This function takes a sorted tuple hand and returns 
    the set of all possible sorted tuples formed by discarding 
    a subset of the entries in hand. 
    The entries in each of these tuples correspond to the dice 
    that will be held.
    """
#    holds = set([()])
#    for die in hand:
#        for partial_sequence in holds:   
#            new_hold = list(partial_sequence)    
#            new_hold.append(die)
#            holds.add(tuple(new_hold))
#    return holds
    all_holds = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for partial_sequence in all_holds:
            new_sequence = list(partial_sequence)
            new_sequence.append(hand[dummy_idx])
            temp_set.add(tuple(new_sequence))
        all_holds = all_holds.union(temp_set)
    return all_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    
    This function takes a sorted tuple hand and 
    computes which dice to hold to maximize the expected value 
    of the score of the possible hands that result 
    from rolling the remaining free dice 
    (with the specified number of sides). 
    The function should return a tuple consisting of 
    this maximal expected value and the choice of dice 
    (specified as a sorted tuple) that should be held to 
    achieve this value. 
    If there are several holds that generate the maximal 
    expected value, you may return any of these holds.
    """
    all_holds = gen_all_holds(hand)
    max_expectation = 0.0
    max_hold = ()
    for hold in all_holds:
        num_free_dice = len(hand) - len(hold)        
        expectation = expected_value(hold, num_die_sides, num_free_dice)
        if expectation > max_expectation:
            max_expectation = expectation
            max_hold = hold        
    return (max_expectation, max_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
#run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



