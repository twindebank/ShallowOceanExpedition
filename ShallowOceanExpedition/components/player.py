from random import randint

from ShallowOceanExpedition.utils.exceptions import Cheating
from ShallowOceanExpedition.utils.logging import logger, TURN, ROUND


class Player:
    def __init__(self, strategy):
        self.name = strategy.player_name
        self.position = 0
        self.tiles = []
        self.direction = 1
        self.bank = 0
        self.n_turn = 0
        self.strategy = strategy
        self.back_home = False
        self.deaths = []

    @property
    def is_home(self):
        return True if self.position == 0 and self.direction == -1 else False

    def roll(self):
        roll = (randint(1, 3) + randint(1, 3))
        moves = max(roll - self.count_tiles(), 0)
        logger.log(TURN, f'- {self.name} rolled a {roll} {"forward" if self.direction>0 else "backward"}'
                         f': move {moves}!')
        return moves

    def collect_tile(self, tile):
        if tile.level is None:
            raise ValueError('Cant pick up blank tile.')
        self.tiles.append(tile)

    def drop_tile(self, tile_level):
        if not self.tiles:
            raise ValueError('No tiles to drop.')
        tile_index_to_drop = [tile.level for tile in self.tiles].index(tile_level)
        return self.tiles.pop(tile_index_to_drop)

    def count_tiles(self):
        return len(self.tiles)

    def summarise_tiles(self):
        tile_levels = [tile.level for tile in self.tiles]
        return {level: tile_levels.count(level) for level in set(tile_levels)}

    def change_direction(self):
        logger.log(TURN, f'- {self.name} changed direction!')
        if self.direction == -1:
            raise Cheating('You cant turn around again you cheating bugger!')
        self.direction = -1

    def kill(self):
        if self.back_home:
            raise Cheating('Player already home.')
        logger.log(ROUND, f"- {self.name} didn't make it, they lost {self.count_tiles()} tiles :-(")
        dropped_tiles = self.tiles
        self.clear_player()
        return dropped_tiles

    def reached_home(self):
        if self.back_home:
            raise Cheating('Player already home.')
        logger.log(ROUND, f"{self.name} made it!!")
        self.back_home = True
        self.bank += self.get_tile_values()
        self.clear_player()

    def clear_player(self):
        self.tiles = []
        self.position = 0
        self.direction = 1
        self.n_turn = 0
        self.deaths.append(not self.back_home)

    def get_tile_values(self):
        if not self.back_home:
            raise Cheating('This method cannot be called whilst the player is playing!')
        return sum(tile.value for tile in self.tiles)

    def __str__(self):  # pragma: no cover
        return f"""- Summary for {self.name}:
  * Tiles: {self.summarise_tiles()}
  * Position: {self.position}
  * Bank: {self.bank}
  * Turn number: {self.n_turn}
  * Direction: {"forward" if self.direction>0 else "backward"}"""

    def __repr__(self):  # pragma: no cover
        return self.name
