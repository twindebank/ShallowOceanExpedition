from copy import copy
from itertools import cycle
from random import randint, choice


class RoundOver(Exception):
    pass


class Cheating(Exception):
    pass


class PlayerHome(Exception):
    pass


class Board:
    def __init__(self, players, tiles=None):
        self.tiles = tiles if tiles else [Tile(1)] * 5 + [Tile(2)] * 5 + [Tile(3)] * 5 + [Tile(4)] * 5
        self.players = players
        self.oxygen = 25
        self.player_cycle = cycle(players)
        self.current_player = next(self.player_cycle)
        print(f'Welcome players {", ".join([player.name for player in self.players])}')
        for player in players:
            print(player)

    def take_turn(self):
        if self.current_player.playing:
            self._reduce_ox(self.current_player.count_tiles())
            landed_on = self._advance_current_player()
            if landed_on is not None:
                if landed_on.level == 0:
                    self._apply_current_player_tile_drop_strategy(landed_on)
                else:
                    self._apply_current_player_tile_collect_strategy(landed_on)
                self._apply_current_player_direction_strategy()
                print(self.current_player)
        self._next_player()

    def has_players(self):
        return sum(player.playing for player in self.players)

    def _advance_current_player(self):
        roll = self.current_player.roll()
        new_position = self._calculate_new_position(roll)
        self.current_player_position = new_position
        self.current_player.n_turn += 1
        if new_position <= 0:
            self.current_player.save()
            return None
        return self.tiles[new_position]

    def _calculate_new_position(self, roll):
        other_positions = self._get_other_player_positions()
        curr_position = self.current_player_position
        for other_player_pos in other_positions:
            if curr_position <= other_player_pos <= curr_position + roll:
                roll += 1
        return min(curr_position + roll, len(self.tiles))

    @property
    def current_player_position(self):
        return self.current_player.position

    @current_player_position.setter
    def current_player_position(self, new_position):
        self.current_player.position = new_position

    @property
    def current_player_tile_at_position(self):
        return self.tiles[self.current_player_position]

    def _get_other_player_positions(self):
        return [player.position for player in self.players if player is not self.current_player]

    def _next_player(self):
        self.current_player = next(self.player_cycle)
        if self.current_player.playing:
            print(f"It's {self.current_player.name}'s go!")

    def _reduce_ox(self, n):
        if n > 0:
            print(f'{self.current_player.name} has {self.current_player.count_tiles()} tile(s), oxygen reduced from '
                  f'{self.oxygen} to {self.oxygen - n}')
        self.oxygen -= n
        if self.oxygen < 0:
            # kill all players
            dropped_tiles = {}
            for player in self.players:
                if player.playing:
                    dropped = player.kill()
                    dropped_tiles[player.position] = dropped
            ordered_stacks = [dropped_tiles[player_n] for player_n in sorted(dropped_tiles)]
            self.reduce_board(ordered_stacks)
            self.next_round()

    def reduce_board(self, ordered_stacks):
        # need to process stacks of tiles into new single tiles
        self.tiles = [tile for tile in self.tiles if tile.level != 0]
        self.tiles.extend(ordered_stacks)

    def next_round(self):
        # choose correct next player then whammer
        raise Exception('Next round not implemented yet.')

    def _apply_current_player_tile_collect_strategy(self, landed_on_tile):
        player_collected = self.current_player.strategy.tile_collect(landed_on_tile, self.current_player)
        if player_collected:
            self.tiles[self.current_player_position] = Tile(0)
            print(f'{self.current_player.name} picked up a level {landed_on_tile.level} tile!!')

    def _apply_current_player_tile_drop_strategy(self, landed_on_tile):
        tile_to_drop = self.current_player.strategy.tile_drop(landed_on_tile, self.current_player)
        if tile_to_drop:
            self.tiles[self.current_player_position] = tile_to_drop

    def _apply_current_player_direction_strategy(self):
        self.current_player.strategy.decide_direction(self.current_player)


class Tile:
    def __init__(self, level):
        self.level = level
        self.__value = None
        if level == 0:
            self.value_range = [0]
        elif level == 1:
            self.value_range = range(0, 5)
        elif level == 2:
            self.value_range = range(5, 10)
        elif level == 3:
            self.value_range = range(10, 15)
        elif level == 4:
            self.value_range = range(15, 20)
        else:
            raise ValueError('Level must be one of [1,2,3,4]')

    @property
    def value(self):
        if self.__value is None:
            self.__value = choice(self.value_range)
        return self.__value


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.position = 0
        self.__tiles = []
        self.direction = 1
        self.bank = 0
        self.n_turn = 0
        self.strategy = strategy
        self.playing = True

    def roll(self):
        roll = (randint(1, 3) + randint(1, 3))
        moves = max(roll - self.count_tiles(), 0)
        print(f'{self.name} rolled a {roll} {"forward" if self.direction>0 else "backward"}, so moves {moves}!')
        return self.direction*moves

    @property
    def tiles(self):
        return copy(self.__tiles)

    def add_tile(self, tile):
        self.__tiles.append(tile)

    def drop_tile(self, index):
        return self.__tiles.pop(index)

    def count_tiles(self):
        return len(self.tiles)

    def summarise_tiles(self):
        tile_levels = [tile.level for tile in self.tiles]
        return {f'Level {level}': tile_levels.count(level) for level in sorted(set(tile_levels))}

    def change_direction(self):
        print(f'{self.name} changed direction!')
        if self.direction == -1:
            raise Cheating('You cant turn around again you cheating bugger!')
        self.direction = -1

    def kill(self):
        print(f"{self.name} didn't make it, they lost {self.count_tiles()} tiles :-(")
        dropped_tiles = self.__tiles
        self.__tiles = []
        return dropped_tiles

    def get_tile_values(self):
        return sum(tile.value for tile in self.tiles)

    def save(self):
        if self.position > 0:
            raise Cheating("You're not home you cheating bugger.")
        self.playing = False
        print(f"{self.name} made it!!")
        value = self.get_tile_values()
        self.__tiles = []
        self.bank += value

    def __str__(self):
        return f"""Summary for {self.name}:
    Tiles: {self.summarise_tiles()}
    Position: {self.position}
    Bank: {self.bank}
        """


class DefaultStrategy:
    # should receive read only views of own player and view of board
    def __init__(self):
        self.direction_changed = False

    def decide_direction(self, player):
        # should receive read only views of board and player
        if player.n_turn > 1 and not self.direction_changed:
            player.change_direction()
            self.direction_changed = True

    def tile_collect(self, tile, player):
        player.add_tile(tile)
        return True

    def tile_drop(self, tile, player):
        # dont drop any
        return None


def main():
    players = [Player('Theo', DefaultStrategy()), Player('Tati', DefaultStrategy())]
    board = Board(players)
    while board.has_players():
        board.take_turn()


if __name__ == '__main__':
    main()
