# Yahtzee

Yahtzee is a dice game played with 5 dice where you try to score the most points by matching certain combinations. 
In Yahtzee, you get to roll the dice three times on each turn. 
After the first roll, you may hold as many dice as you would like and roll the remaining free dice. 
After the second roll, you may again hold as many dice as you would like and roll the rest. 
Once you stop (either because you have exhausted your three rolls or you are satised with the dice you have), 
you score the dice in one box on the score card.

For this project, we will implement a strategy function designed to help you choose which dice to hold 
after your second roll during the first turn of a game of Yahtzee. 
This function will consider all possible choices of dice to hold and recommend the choice 
that maximizes the expected value of your score after the nal roll.

To simplify the project, we will only consider scores corresponding to the "upper" section of the scorecard. 
Boxes in the upper section correspond to numbers on the dice. 
After each turn, you may choose one empty box and enter the sum of the dice you have with the corresponding number. 
For example, if you rolled (2,3,3,3,4), you could score 2 in the "Twos" box, 9 in the "Threes" box, or 4 in the "Fours" box.

To play, please open the url in browser: 
http://www.codeskulptor.org/#user43_fQ7r9WaXCw_5.py
