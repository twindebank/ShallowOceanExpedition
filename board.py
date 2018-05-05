from itertools import cycle

from exceptions import RoundOver
from tiles import Submarine, TileStack, Tile


class Board:
    def __init__(self, players, oxygen=25, n_level_1=5, n_level_2=5, n_level_3=5, n_level_4=5):
        self.players = players
        self.tiles = \
            [Submarine()] + \
            [Tile(1)] * n_level_1 + \
            [Tile(2)] * n_level_2 + \
            [Tile(3)] * n_level_3 + \
            [Tile(4)] * n_level_4
        self.round_number = 0
        self.original_oxygen = oxygen
        self.oxygen = oxygen
        self.player_cycle = cycle(players)
        self.current_player = next(self.player_cycle)
        print(f'Welcome players {", ".join([player.name for player in players])} for round {self.round_number}!!')
        for player in players:
            print(player)

    def take_turn(self):
        if not self.current_player.finished:
            print(f"\nIt's {self.current_player.name}'s go!")
            self._reduce_ox_by(self.current_player.count_tiles())
            self._apply_current_player_direction_strategy()
            landed_on = self._advance_current_player()
            if landed_on is not None:
                if landed_on.level == 0:
                    self._apply_current_player_drop_strategy()
                else:
                    self._apply_current_player_collect_strategy(landed_on)
            print(self.current_player)
        self._next_player()

    def has_players(self):
        return bool(sum(not player.finished for player in self.players))

    def end_game_summary(self):
        print('\nGame over!')
        banks = {player.name: player.bank for player in self.players}
        winner = max(banks, key=banks.get)
        print(f'The winner is {winner} with a score of {banks[winner]}!!')
        del banks[winner]
        print(f'Other scores: {banks}')

    def _summarise_tile_levels(self):
        return [tile.level for tile in self.tiles]

    def _apply_current_player_collect_strategy(self, landed_on):
        do_pickup = self.current_player.strategy.tile_collect(*self._strategy_summary())
        if do_pickup:
            self.current_player.collect_tile(landed_on)
            self.tiles[self._current_player_position] = Tile(0)
            print(f'- {self.current_player.name} picked up a level {landed_on.level} tile!!')

    def _apply_current_player_drop_strategy(self):
        do_drop = self.current_player.strategy.tile_drop(*self._strategy_summary())
        if do_drop:
            dropped = self.current_player.drop_tile()
            self.tiles[self._current_player_position] = dropped

    def _advance_current_player(self):
        roll = self.current_player.roll()
        new_position = self._calculate_new_position(roll)
        self._current_player_position = new_position
        self.current_player.n_turn += 1
        if self._current_player_position == 0:
            self.current_player.finished = True
            self.current_player.bank_tiles()
            return None
        return self.tiles[new_position]

    def _calculate_new_position(self, roll):
        other_positions = [pos for pos in self._get_other_player_positions() if pos > 0]
        curr_position = self._current_player_position
        for other_player_pos in other_positions:
            if curr_position <= other_player_pos <= curr_position + roll:
                roll += 1
        return max(0, min(curr_position + roll, len(self.tiles) - 1))

    @property
    def _current_player_position(self):
        return self.current_player.position

    @_current_player_position.setter
    def _current_player_position(self, new_position):
        self.current_player.position = new_position

    @property
    def _current_player_tile_at_position(self):
        return self.tiles[self._current_player_position]

    def _get_other_player_positions(self):
        return [player.position for player in self.players if player is not self.current_player]

    def _get_other_players(self):
        return [player for player in self.players if player is not self.current_player]

    def _next_player(self):
        self.current_player = next(self.player_cycle)

    def _reduce_ox_by(self, n):
        if n > 0:
            print(f'- {self.current_player.name} has {self.current_player.count_tiles()} tile(s), oxygen reduced from '
                  f'{self.oxygen} to {self.oxygen - n}')
        self.oxygen -= n
        if self.oxygen < 0:
            self._oxygen_depleted()

    def _oxygen_depleted(self):
        print('\nOxygen depleted!')
        dropped_tiles = {}
        for player in self.players:
            if not player.finished:
                dropped = player.kill()
                dropped_tiles[player.position] = TileStack(dropped)

        ordered_stacks = [dropped_tiles[player_n] for player_n in sorted(dropped_tiles, reverse=True)]
        self._reduce_board(ordered_stacks)
        self.round_number += 1
        self.oxygen = self.original_oxygen
        self._reset_players()
        print('Round over, player summaries:')
        for player in self.players:
            print(player)
        raise RoundOver('Round over!')
        # TODO: sort out ordering of players for new round

    def _reset_players(self):
        for player in self.players:
            player.reset(game_finished=True)

    def _reduce_board(self, ordered_stacks):
        # need to process stacks of tiles into new single tiles
        self.tiles = [tile for tile in self.tiles if tile.level != 0]
        self.tiles.extend(ordered_stacks)

    def _apply_current_player_direction_strategy(self):
        do_change = self.current_player.strategy.decide_direction(*self._strategy_summary())
        if do_change:
            self.current_player.change_direction()

    def _strategy_summary(self):
        player = {
            'tiles': self.current_player.summarise_tiles(),
            'position': self.current_player.position,
            'bank': self.current_player.bank,
            'changed_direction': False if self.current_player.direction > 0 else True,
            'turn_number': self.current_player.n_turn
        }
        board = {
            'tiles': self._summarise_tile_levels(),
            'round_number': self.round_number
        }
        other_players = {
            player.name: {
                'tiles': self.current_player.summarise_tiles(),
                'position': self.current_player.position,
                'bank': self.current_player.bank,
                'changed_direction': True if self.current_player.direction > 0 else False,
                'turn_number': self.current_player.n_turn
            } for player in self._get_other_players()
        }
        return player, board, other_players





