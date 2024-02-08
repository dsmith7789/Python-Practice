# Overview
These are some personal projects I've worked on that I used to practice implementing Python practically. 

## Alien Game
This project is based on the project in chapters 12-14 of "Python Crash Course, 2nd edition". Some modifications that I added:
* Pause game functionality
* Notifications during a break between levels (make it more obvious to players a level was advanced)
* Persistent saving of high scores
* A top 10 scores leaderboard. I use a heap behind the scenes to order the scores high-to-low and handle removing the bottom score, if your score beats it in the top 10.