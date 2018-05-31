# Shallow Ocean Expedition :ocean: :ship:

Simulate runs of a game with the ability to define custom strategies. 
Written in Python 3.6.

## Setup
Install requirements:`pip install -r requirements.txt`

## Run
To run the examples included: 
- `python -m examples.example_game_manager` for an example of 
how to simulate a number of games and gather/plot statistics. 
This example will run 1000 simulations and rotate the order of the players, output plot will be saved to `wins.png` in the root directory of the package.
- `python -m examples.example_game` for an example of how to 
run a single game with a more verbose output.

## Strategies
Create a class inheriting from `game.components.strategy.DefaultStrategy` and override the methods.


## ToDo
- More documentation/examples of custom strategies
    * include examples of dicts to work with
- Handle results when tie
- account for cases where nobody wins
- Tests
- Docstrings
- Add more kinds of plots
    * plots of 1st/2nd/3rd per player
- add automated testing in setup.py
- add GameServer for strategies to be submitted and ranked against others
    * server holds number of stategies (can be more than 6)
    * on submission of new strategies, server does all perms and combs of players (up to 6 players per game) and stores total number of wins
- profile code and speed up

## Notes
Install branch with pip install https://github.com/twindebank/ShallowOceanExpedition/archive/BRANCH.zip --upgrade
