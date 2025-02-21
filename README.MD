This is my first published python project which I have built from scrtach. This project was to test out the functionalities of the monte carlo simulation in different poker scenario by calculating equity (win odds). A few things to take into account:

* Install the pillow library
* Unzip the cards file

The project has 3 main code blocks:

1. win_rank():

This code block calculates the win rank of a given hand on a given board texture. So for example, if given the hand [A♥, K♥] with the board texture [3♥, 7♥, 7♣, T♥, A♣] it is able to recognise that this hand has achieved a flush. 

The code block also calculates the internal win rank by assigning values. So for example take the same hand of [A♥, K♥] with the same board texture [3♥, 7♥, 7♣, T♥, A♣], it assigns a win value to this Ace high flush and all the cards in the flush set. It does so by assigning a number and will be used in the next code block when comparing one card against another.

2. multi_way_equity():

This code block runs the monte carlo simualation and takes into account multiple parameters, these include:

~ Simul: Number of times the simulation will occur.
~ Player Card Set: The hole cards of all the players playing.
~ Community Cards: Not compulsary to be present but includes community cards if user wishes to simulate a scenrio with certain community cards present.
~ Dead Cards: Removes the provided cards from the deck for the simulation.

For each simulation, it takes into account which player has won or which players have tied.

3. PokerTableGUI:

This code block is the GUI for the app and was primarly built using ChatGPT. It consists of the following features:

~ A deck of 52 cards with colour coding
~ Table set with placeholders for the hole cards of 9 players
~ A dead card set with places for 16 cards
~ A select feature to choose cards in the placeholders
~ A deselect feature to return the cards back to their original position if clicked on when inside a placeholder
~ A New Hand button to return all cards to their original deck position
~ A Calculate Equity button to calculate equity for all players and display errors if insufficient cards have been inputted
~ A slider to adjust the number of times the simulation will occur

## Major inspirations from this website (https://www.cardplayer.com/poker-tools/odds-calculator/texas-holdem)

This was a true passion project of mine and I would love to continue doing projects like these :).