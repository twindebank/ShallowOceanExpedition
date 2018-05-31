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
- Package the module so it can be installed
- Tests
- Docstrings
- Add more kinds of plots
- account for cases where nobody wins
- add automated testing in setup.py

## Notes
Install branch with pip install https://github.com/twindebank/ShallowOceanExpedition/archive/BRANCH.zip --upgrade
