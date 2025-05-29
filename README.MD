This is my updated publish of my first python project which I have built from scrtach. This project was to test out the functionalities of the monte carlo simulation in different poker scenario by calculating equity (win odds). A few things to take into account:

* Install the pillow library
* Unzip the cards file

The project has 4 main code blocks:

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

3. hand_v_range():

This code block assimilates all the possible card combination the opponent (villain) can have and matches them up against the given combination of the hero. 

This block shares the same parameters as multi_way_equity() however it has the added x_inp parameter, it tackles:

~ Card combination creation: For example pocket 44 can be represented as 4 of hearts, 4 of spades then 4 of spades, 4 of clubs and so on
~ Suitedness: If a card combination is suited it can generate the necessary suited combos for those cards, similarly it can do so for unsuited combos as well

3. PokerTableGUI:

This code block is the GUI for the app and was primarly built using ChatGPT. It consists of the following features:

~ A deck of 52 cards with colour coding
~ Table set with placeholders for the hole cards of a single player
~ A dead card set with places for 16 cards
~ A select feature to choose cards in the placeholders
~ A deselect feature to return the cards back to their original position if clicked on when inside a placeholder
~ A New Hand button to return all cards to their original deck position
~ A range table with possible range of hands that the villain can have (select and desselect options available)
~ Preset range options with drop-down feature for different positions
~ A Calculate Equity button to calculate equity for all players and display errors if insufficient cards have been inputted
~ A slider to adjust the number of times the simulation will occur

## GUI inspirations from this website (https://www.cardplayer.com/poker-tools/odds-calculator/texas-holdem) and this (https://openpokertools.com/equity/)

This is a true passion project of mine and I am loving projects like these :).
