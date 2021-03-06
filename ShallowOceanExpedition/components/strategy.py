from ShallowOceanExpedition.utils.exceptions import RuleViolation


class DefaultStrategy:
    def __init__(self, player_name):
        self.player_name = player_name

    @staticmethod
    def decide_direction(player, board, others):
        # should receive read only views of board_2p and player
        if board['round_number'] in [0, 1]:
            # start risky
            change = True if player['turn_number'] > 2 and not player['changed_direction'] else False
        elif board['round_number'] == 2:
            # reduce risk for last go
            change = True if player['turn_number'] > 1 and not player['changed_direction'] else False
        else:
            raise RuleViolation()
        return change

    @staticmethod
    def tile_collect(player, board, others):
        if board['round_number'] in [0, 1]:
            # start risky
            change = True if player['turn_number'] > 1 else False
        elif board['round_number'] == 2:
            # reduce risk for last go
            change = True if player['turn_number'] > 0 else False
        else:
            raise RuleViolation()
        return change

    @staticmethod
    def tile_drop(player, board, others):
        if player['position'] >= 5 and len(player['tiles']) >= 2 and board['oxygen'] <= 10:
            tile_levels = list(player['tiles'].keys())
            flat_tile_levels = [level if isinstance(level, int) else sum(level) for level in tile_levels]
            min_tile_level = tile_levels[flat_tile_levels.index(min(flat_tile_levels))]
            return True, min_tile_level
        return False, None
