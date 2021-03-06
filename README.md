# Shallow Ocean Expedition :ocean: :ship: [![Build Status](https://semaphoreci.com/api/v1/twindebank/shallowoceanexpedition/branches/master/badge.svg)](https://semaphoreci.com/twindebank/shallowoceanexpedition)

[![Maintainability](https://api.codeclimate.com/v1/badges/d10f25e10c37e86728fb/maintainability)](https://codeclimate.com/github/twindebank/ShallowOceanExpedition/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d10f25e10c37e86728fb/test_coverage)](https://codeclimate.com/github/twindebank/ShallowOceanExpedition/test_coverage)

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


## ToDo/Bugs
- tests
- add setup.cfg
- set up with coveralls, drone, etc
- profile code and speed up
- have a play_game method in board rather than game manager

## Planned Features
- have a rules.py file to define game rules like number of rounds, number of tiles of which type, etc...
- More documentation/examples of custom strategies
    * include examples of dicts to work with
- docs of logging level
- Docstrings
- Add more kinds of plots
    * plots of 1st/2nd/3rd per player
- add automated testing in setup.py
- add GameServer for strategies to be submitted and ranked against others
    * server holds number of stategies (can be more than 6)
    * on submission of new strategies, server does all perms and combs of players (up to 6 players per game) and stores total number of wins
- stats per player averaged over all games eg times died in round one, times died in round two, number of times dropped tiles etc

## Notes
Install branch with pip install git+https://github.com/twindebank/ShallowOceanExpedition@BRANCH 

