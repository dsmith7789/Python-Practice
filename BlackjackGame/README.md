# Blackjack
I've implemented a text-based blackjack game before [(see Black-Jack)](https://github.com/dsmith7789/Black-Jack/tree/main), but I wanted to try a graphical based version of the game taking what I learned from the book-guided Alien Game. So, this is a more self-guided project where I had to think through the design of the game based on the rules and how I've seen the game played in real life.

## Project Setup
Like the last project, I used developed in a virtual environment to avoid package version conflicts. To do this, navigate to the directory you cloned the repo to and use the command:
`python3 -m venv venv`

Then activate the virtual environment using the command:
`source venv/bin/activate`

With the virtual environment active, Python packages you install will be limited to only this environment. The virtual environment can be deactivated at any time using the command:
`deactivate`

With the virtual environment activated, you can install all the required packages using the command:
`pip install -r requirements.txt`

Basically this iterates through the lines in the `requirements.txt` file and installs the specific version of the package on that line.

## TO-DO
* Dynamically calculate the placement of the "Deck"
* Get hands to display on the same center point, no matter how many cards in the hand.
* Successfully display the dealer's and player's hand to the screen.
* Display the dealer's hand initially as one face-up, one hidden card
* While it is the player's turn, display a pop-up with 2 buttons, allowing them to hit/stay
* Re-display the pop-up after each turn
* Flip the dealer's 2nd card to be visible after the player has "stayed"
* Display the score of the player's hand at all times
* Display the score of the dealer's hand after their 2nd card has been revealed.
* Have some end-game screen (when a player busts, if the player has won/lost)
* (Nice to have) use some "flip" animation when dealing cards from the deck