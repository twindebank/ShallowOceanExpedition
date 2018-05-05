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
    def __init__(self, players, oxygen=25, n_level_1=5, n_level_2=5, n_level_3=5, n_level_4=5):
        self.players = [Player(player_name, strategy, self) for player_name, strategy in players.items()]
        self.tiles = \
            [Submarine()] + \
            [Tile(1)] * n_level_1 + \
            [Tile(2)] * n_level_2 + \
            [Tile(3)] * n_level_3 + \
            [Tile(4)] * n_level_4
        self.round_number = 0
        self.original_oxygen = oxygen
        self.oxygen = oxygen
        self.player_cycle = cycle(self.players)
        self.current_player = next(self.player_cycle)
        print(f'Welcome players {", ".join([player.name for player in self.players])} for round {self.round_number}!!')
        for player in self.players:
            print(player)

    def take_turn(self):
        if self.current_player.playing:
            print(f"\nIt's {self.current_player.name}'s go!")
            self._reduce_ox(self.current_player.count_tiles())
            self._apply_current_player_direction_strategy()
            landed_on = self._advance_current_player()
            if landed_on is not None:
                if landed_on.level == 0:
                    self._apply_current_player_drop_strategy()
                else:
                    self._apply_current_player_collect_strategy(landed_on)
            print(self.current_player)
        self._next_player()

    def summarise_tile_levels(self):
        return [tile.level for tile in self.tiles]

    def _apply_current_player_collect_strategy(self, landed_on):
        do_pickup = self.current_player.strategy.tile_collect()
        if do_pickup:
            self.current_player.collect_tile(landed_on)
            self.tiles[self.current_player_position] = Tile(0)
            print(f'- {self.current_player.name} picked up a level {landed_on.level} tile!!')

    def _apply_current_player_drop_strategy(self):
        do_drop = self.current_player.strategy.tile_drop()
        if do_drop:
            dropped = self.current_player.drop_tile()
            self.tiles[self.current_player_position] = dropped

    def has_players(self):
        return bool(sum(player.playing for player in self.players))

    def _advance_current_player(self):
        roll = self.current_player.roll()
        new_position = self._calculate_new_position(roll)
        self.current_player_position = new_position
        self.current_player.n_turn += 1
        if self.current_player_position == 0:
            self.current_player.bank_tiles()
            return None
        return self.tiles[new_position]

    def _calculate_new_position(self, roll):
        other_positions = [pos for pos in self._get_other_player_positions() if pos > 0]
        curr_position = self.current_player_position
        for other_player_pos in other_positions:
            if curr_position <= other_player_pos <= curr_position + roll:
                roll += 1
        return max(0, min(curr_position + roll, len(self.tiles) - 1))

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

    def get_other_players(self):
        return [player for player in self.players if player is not self.current_player]

    def _next_player(self):
        self.current_player = next(self.player_cycle)

    def _reduce_ox(self, n):
        if n > 0:
            print(f'- {self.current_player.name} has {self.current_player.count_tiles()} tile(s), oxygen reduced from '
                  f'{self.oxygen} to {self.oxygen - n}')
        self.oxygen -= n
        if self.oxygen < 0:
            self.oxygen_depleted()

    def oxygen_depleted(self):
        print('\nOxygen depleted!')
        dropped_tiles = {}
        for player in self.players:
            if player.playing:
                dropped = player.kill()
                dropped_tiles[player.position] = TileStack(dropped)
            else:
                player.reset_player()

        ordered_stacks = [dropped_tiles[player_n] for player_n in sorted(dropped_tiles, reverse=True)]
        self.reduce_board(ordered_stacks)
        self.round_number += 1
        self.oxygen = self.original_oxygen
        print('Round over, player summaries:')
        for player in self.players:
            print(player)
        raise RoundOver('Round over!')
        # TODO: sort out ordering of players for new round
        # TODO: sort out resetting of players for new round
        #   - board needs to reset all players regardless of wether ox runs out or not

    def reduce_board(self, ordered_stacks):
        # need to process stacks of tiles into new single tiles
        self.tiles = [tile for tile in self.tiles if tile.level != 0]
        self.tiles.extend(ordered_stacks)

    def _apply_current_player_direction_strategy(self):
        do_change = self.current_player.strategy.decide_direction()
        if do_change:
            self.current_player.change_direction()


class Submarine:
    def __init__(self):
        self.value = None
        self.level = 'Submarine'

    def __repr__(self):
        return """Submarine"""


class TileStack:
    def __init__(self, tiles):
        self._tiles = tiles
        self.level = tuple(tile.level for tile in tiles)
        self.__value = None

    @property
    def value(self):
        if self.__value is None:
            self.__value = sum([tile.value for tile in self._tiles])

    def __repr__(self):
        return f"""Level: {self.level}"""


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

    def __repr__(self):
        return f"""Level: {self.level}"""


def player_must_be_finished(attempted_func):
    def raise_if_cheating(player, *args, **kwargs):
        if player.playing:
            raise Cheating('This method cannot be called whilst the player is playing!')
        else:
            return attempted_func(player, *args, **kwargs)

    return raise_if_cheating


class Player:
    def __init__(self, name, strategy, board):
        self.name = name
        self.position = 0
        self.tiles = []
        self.direction = 1
        self.bank = 0
        self.n_turn = 0
        self.strategy = strategy(self, board)

    @property
    def playing(self):
        return False if self.position == 0 and self.direction == -1 else True

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
        return {level: tile_levels.count(level) for level in sorted(set(tile_levels))}

    def change_direction(self):
        print(f'- {self.name} changed direction!')
        if self.direction == -1:
            raise Cheating('You cant turn around again you cheating bugger!')
        self.direction = -1

    def kill(self):
        print(f"- {self.name} didn't make it, they lost {self.count_tiles()} tiles :-(")
        dropped_tiles = self.tiles
        self.reset_player()
        return dropped_tiles

    def reset_player(self):
        self.tiles = []
        self.position = 0
        self.direction = 1
        self.n_turn = 0

    @player_must_be_finished
    def get_tile_values(self):
        return sum(tile.value for tile in self.tiles)

    @player_must_be_finished
    def bank_tiles(self):
        print(f"{self.name} made it!!")
        value = self.get_tile_values()
        self.bank += value

    def __str__(self):
        return f"""- Summary for {self.name}:
  * Tiles: {self.summarise_tiles()}
  * Position: {self.position}
  * Bank: {self.bank}
  * Turn number: {self.n_turn}
  * Direction: {"forward" if self.direction>0 else "backward"}"""

    def __repr__(self):
        return self.name


class DefaultStrategy:
    def __init__(self, player, board):
        self._player = player
        self._board = board

    def decide_direction(self):
        # should receive read only views of board and player
        me, board, others = self.game_info
        change = True if me['turn_number'] > 1 and not me['changed_direction'] else False
        return change

    def tile_collect(self):
        me, board, others = self.game_info
        # pick all up
        return True

    def tile_drop(self):
        me, board, others = self.game_info
        # dont drop any
        return False

    @property
    def game_info(self):
        me = {
            'tiles': self._player.summarise_tiles(),
            'position': self._player.position,
            'bank': self._player.bank,
            'changed_direction': False if self._player.direction > 0 else True,
            'turn_number': self._player.n_turn
        }
        other_players = {
            player.name: {
                'tiles': player.summarise_tiles(),
                'position': player.position,
                'bank': player.bank,
                'changed_direction': True if player.direction > 0 else False,
                'turn_number': player.n_turn
            } for player in self._board.get_other_players()
        }
        board = {
            'tiles': self._board.summarise_tile_levels(),
            'round_number': self._board.round_number
        }
        return me, board, other_players


def main():
    players = {
        'Theo': DefaultStrategy,
        'Tati': DefaultStrategy
    }
    board = Board(players)
    play_round(board)
    play_round(board)
    play_round(board)
    print('Done!')


def play_round(board):
    while board.has_players():
        try:
            board.take_turn()
        except RoundOver:
            break


if __name__ == '__main__':
    main()
