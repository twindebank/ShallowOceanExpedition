from random import randint

from board import player_must_be_finished
from exceptions import Cheating


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.position = 0
        self.tiles = []
        self.direction = 1
        self.bank = 0
        self.n_turn = 0
        self.strategy = strategy
        self.finished = False

    @property
    def is_home(self):
        return True if self.position == 0 and self.direction == -1 else False

    def roll(self):
        roll = (randint(1, 3) + randint(1, 3))
        moves = max(roll - self.count_tiles(), 0)
        print(f'- {self.name} rolled a {roll} {"forward" if self.direction>0 else "backward"}, '
              f'so they have {moves} moves!')
        return self.direction * moves

    def collect_tile(self, tile):
        self.tiles.append(tile)

    def drop_tile(self, index):
        return self.tiles.pop(index)

    def count_tiles(self):
        return len(self.tiles)

    def summarise_tiles(self):
        tile_levels = [tile.level for tile in self.tiles]
        return {level: tile_levels.count(level) for level in set(tile_levels)}

    def change_direction(self):
        print(f'- {self.name} changed direction!')
        if self.direction == -1:
            raise Cheating('You cant turn around again you cheating bugger!')
        self.direction = -1

    def kill(self):
        print(f"- {self.name} didn't make it, they lost {self.count_tiles()} tiles :-(")
        dropped_tiles = self.tiles
        self.reset()
        return dropped_tiles

    def reset(self, game_finished=False):
        self.tiles = []
        self.position = 0
        self.direction = 1
        self.n_turn = 0
        self.finished = not game_finished

    @player_must_be_finished
    def get_tile_values(self):
        return sum(tile.value for tile in self.tiles)

    @player_must_be_finished
    def bank_tiles(self):
        print(f"{self.name} made it!!")
        value = self.get_tile_values()
        self.bank += value
        self.finished = True

    def __str__(self):
        return f"""- Summary for {self.name}:
  * Tiles: {self.summarise_tiles()}
  * Position: {self.position}
  * Bank: {self.bank}
  * Turn number: {self.n_turn}
  * Direction: {"forward" if self.direction>0 else "backward"}"""

    def __repr__(self):
        return self.name