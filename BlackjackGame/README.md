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

## Interesting Lessons
### Default mutable arguments in function definitions
I was seeing an odd bug where the hands would have the same cards, even though the Hand and Player objects were definitely different. This was because of my initial constructor for the Hand class:

`class Hand: def __init__(self, cards: Optional[list[Card]]=[]):`

The default value of `[]` was being shared across all calls to the function. This meant that when the default value was modified (e.g. adding a card), those modifications were showing up in all the lists of cards, meaning both hands would always have the same cards.

**SOLUTION:** Use the list() constructor, e.g. (`self.cards = list(cards)`) which will create a deep copy of the argument and set the self.cards array to that list copy, which will be guaranteed to be a new object in memory from the default list.

## TO-DO
* :white_check_mark: Dynamically calculate the placement of the "Deck"
* :white_check_mark: Don't allow unlimited hits
* :white_check_mark: Get hands to display on the same center point, no matter how many cards in the hand.
* :white_check_mark: Successfully display the dealer's and player's hand to the screen.
* :white_check_mark: Display the dealer's hand initially as one face-up, one hidden card
* :white_check_mark: While it is the player's turn, display a pop-up with 2 buttons, allowing them to hit/stay
* :white_check_mark: Re-display the pop-up after each turn
* :white_check_mark: Flip the dealer's 2nd card to be visible after the player has "stayed"
* :white_check_mark: Display the score of the player's hand at all times
* :white_check_mark: Display the score of the dealer's hand after their 2nd card has been revealed.
* :white_check_mark: Have some end-game screen (when a player busts, if the player has won/lost)
* :white_check_mark: Calculate the score of a hand with aces correctly
* Add some slow down to simulate the cards coming into the hand?
* (Nice to have) use some "flip" animation when dealing cards from the deck
* Add some session specific score keeping (i.e. in this session, you have won X and computer won Y)
* Add unit tests to the project
* Add logging to the project - Use Observer design pattern here
* Log: Clicks: Count per session and position
* Log: Key Presses: Count per session and which key
* Log: Wins and Losses per session
* Log: Length of time per session
