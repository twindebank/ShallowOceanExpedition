class DefaultStrategy:
    def __init__(self, player_name):
        self.player_name = player_name
    @staticmethod
    def decide_direction(player, board, others):
        # should receive read only views of board and player
        change = True if player['turn_number'] > 1 and not player['changed_direction'] else False
        return change

    @staticmethod
    def tile_collect(player, board, others):
        # pick all up
        return True

    @staticmethod
    def tile_drop(player, board, others):
        # dont drop any
        return False