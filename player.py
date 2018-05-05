from random import randint

from exceptions import Cheating

def player_must_be_finished(attempted_func):
    def raise_if_cheating(player, *args, **kwargs):
        if not player.finished:
            raise Cheating('This method cannot be called whilst the player is playing!')
        else:
            return attempted_func(player, *args, **kwargs)

    return raise_if_cheating

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
        self.killed = False
        self.deaths = []

    @property
    def is_home(self):
        return True if self.position == 0 and self.direction == -1 else False

    def roll(self):
        roll = (randint(1, 3) + randint(1, 3))
        moves = max(roll - self.count_tiles(), 0)
        print(f'- {self.name} rolled a {roll} {"forward" if self.direction>0 else "backward"}'
              f': move {moves}!')
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
        self.killed = True
        return dropped_tiles

    def soft_reset(self):
        self.tiles = []
        self.position = 0
        self.direction = 1
        self.n_turn = 0
        self.finished = False
        self.deaths.append(self.killed)
        self.killed = False

    def hard_reset(self):
        self.soft_reset()
        self.bank = 0

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


