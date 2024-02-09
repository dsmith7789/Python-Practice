# Blackjack
I've implemented a text-based blackjack game before, but I wanted to try a graphical based version of the game taking what I learned from the book-guided Alien Game. So, this is a more self-guided project where I had to think through the design of the game based on the rules and how I've seen the game played in real life.

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
