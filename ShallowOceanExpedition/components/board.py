from itertools import cycle

from ShallowOceanExpedition.components.player import Player
from ShallowOceanExpedition.components.tiles import Home, TileStack, Tile, BlankTile
from ShallowOceanExpedition.utils.exceptions import RoundOver
from ShallowOceanExpedition.utils.logging import logger, GAME, TURN, ROUND


class Board:
    def __init__(self, strategies, oxygen=25, n_level_1=5, n_level_2=5, n_level_3=5, n_level_4=5):
        if len(strategies) < 2:
            raise ValueError('Must supply at least two strategies')
        self.players = [Player(strategy) for strategy in strategies]
        self.tiles = \
            [Home()] + \
            [Tile(1)] * n_level_1 + \
            [Tile(2)] * n_level_2 + \
            [Tile(3)] * n_level_3 + \
            [Tile(4)] * n_level_4
        self.round_number = 0
        self.original_oxygen = oxygen
        self.oxygen = oxygen
        self.player_cycle = cycle(self.players)
        self.current_player = next(self.player_cycle)
        logger.log(GAME, f'Welcome players {", ".join([player.name for player in self.players])} for round '
                         f'{self.round_number}!!')
        for player in self.players:
            logger.log(GAME, player)

    def play_round(self):
        while True:
            try:
                self._take_turn()
            except RoundOver:
                break
                # return stats

    def _take_turn(self):
        if not self.current_player.finished:
            logger.log(TURN, f"\nIt's {self.current_player.name}'s go!")
            self._reduce_ox_by(self.current_player.count_tiles())
            self._apply_current_player_direction_strategy()
            landed_on = self._advance_current_player()
            if landed_on is not None:
                if landed_on.level is None:
                    self._apply_current_player_drop_strategy()
                else:
                    self._apply_current_player_collect_strategy(landed_on)
            logger.log(TURN, self.current_player)
        if not self._has_players():
            self._end_round()
        else:
            self._next_player()

    def _has_players(self):
        return bool(sum(not player.back_home for player in self.players))

    def _summarise_tile_levels(self):
        return [tile.level for tile in self.tiles]

    def _apply_current_player_collect_strategy(self, landed_on):
        do_pickup = self.current_player.strategy.tile_collect(*self._summarise_game())
        if do_pickup:
            self.current_player.collect_tile(landed_on)
            self.tiles[self.current_player.position] = BlankTile()
            logger.log(TURN, f'- {self.current_player.name} picked up a level {landed_on.level} tile!!')

    def _apply_current_player_drop_strategy(self):
        do_drop, tile_level = self.current_player.strategy.tile_drop(*self._summarise_game())
        if do_drop:
            dropped = self.current_player.drop_tile(tile_level)
            self.tiles[self.current_player.position] = dropped

    def _apply_current_player_direction_strategy(self):
        do_change = self.current_player.strategy.decide_direction(*self._summarise_game())
        if do_change:
            self.current_player.change_direction()

    def _advance_current_player(self):
        roll = self.current_player.roll()
        new_position = self._calculate_new_position(roll)
        self.current_player.position = new_position
        self.current_player.n_turn += 1
        if self.current_player.position == 0:
            self.current_player.reached_home()
            return None
        return self.tiles[new_position]

    def _calculate_new_position(self, roll):
        other_positions = [pos for pos in self._get_other_player_positions() if pos > 0]
        curr_position = self.current_player.position
        for other_player_pos in other_positions:
            if curr_position <= other_player_pos <= curr_position + roll:
                roll += 1
        return max(0, min(curr_position + roll, len(self.tiles) - 1))

    def _get_other_player_positions(self):
        return [player.position for player in self.players if player is not self.current_player]

    def _get_other_players(self):
        return [player for player in self.players if player is not self.current_player]

    def _next_player(self):
        self.current_player = next(self.player_cycle)

    def _reduce_ox_by(self, n):
        if n > 0:
            logger.log(TURN,
                       f'- {self.current_player.name} has {self.current_player.count_tiles()} tile(s), oxygen reduced '
                       f'from {self.oxygen} to {self.oxygen - n}')
        self.oxygen -= n
        if self.oxygen < 0:
            logger.log(ROUND, '\nOxygen depleted!')
            self._end_round()

    def _end_round(self):
        dropped_tiles = {}
        self._order_players()
        for player in self.players:
            if not player.back_home:
                dropped = player.kill()
                if dropped:
                    dropped_tiles[player.position] = TileStack(dropped)

        ordered_stacks = [dropped_tiles[player_n] for player_n in sorted(dropped_tiles, reverse=True)]
        self._reduce_board(ordered_stacks)
        self.round_number += 1
        self.oxygen = self.original_oxygen
        logger.log(ROUND, f'Round {self.round_number} over, player summaries:')
        for player in self.players:
            logger.log(ROUND, player)
            player.back_home = False
        raise RoundOver('Round over!')

    def _reduce_board(self, ordered_stacks):
        self.tiles = [tile for tile in self.tiles if tile.level != (0,)]
        self.tiles.extend(ordered_stacks)

    def _summarise_game(self):
        player = {
            'tiles': self.current_player.summarise_tiles(),
            'position': self.current_player.position,
            'bank': self.current_player.bank,
            'changed_direction': False if self.current_player.direction > 0 else True,
            'turn_number': self.current_player.n_turn
        }
        board = {
            'tiles': self._summarise_tile_levels(),
            'round_number': self.round_number,
            'oxygen': self.oxygen
        }
        other_players = {
            player.name: {
                'tiles': player.summarise_tiles(),
                'position': player.position,
                'bank': player.bank,
                'changed_direction': True if player.direction > 0 else False,
                'turn_number': player.n_turn
            } for player in self._get_other_players()
        }
        return player, board, other_players

    def print_end_game_summary(self):
        logger.log(GAME, '\nGame over!')
        banks = {player.name: player.bank for player in self.players}
        winner = max(banks, key=banks.get)
        logger.log(GAME, f'The winner is {winner} with a score of {banks[winner]}!!')
        del banks[winner]
        logger.log(GAME, f'Other scores: {banks}')

    def _order_players(self):
        if self._has_players():
            # if player killed then furthest one
            positions = {player.name: player.position for player in self.players}
            last_player = max(positions, key=positions.get)
            while self.current_player.name != last_player:
                self._next_player()

    def get_stats(self):
        banks = sorted([player.bank for player in self.players], reverse=True)
        stats = {}
        for player in self.players:
            stats[player.name] = {
                'score': player.bank,
                'rank': banks.index(player.bank) + 1 if player.bank > 0 else None,
                'deaths': player.deaths
            }
            if len(player.deaths) > 3:
                print('here')
        return stats
