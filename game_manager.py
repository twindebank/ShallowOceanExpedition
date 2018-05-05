from board import Board
from stats import Stats


class Manager:
    stats = []
    # todo: custom logging levels: turn, round, game

    def run_n_rounds(self, n, players, **board_params):
        board = Board(players, **board_params)
        for _ in range(n):
            board.play_round()
        stats = board.get_stats()
        board.print_end_game_summary()
        self.stats.append(stats)

    def run_n_games(self, n, rounds_per_game, players, **board_params):
        for _ in range(n):
            self.run_n_rounds(rounds_per_game, players, **board_params)

    def run_n_games_and_rotate_players(self, n, rounds_per_game, players, **board_params):
        for n_player in range(len(players)):
            self.run_n_games(n, rounds_per_game, players, **board_params)
            players = [players.pop()] + players
        print('Done!')

    def run_n_games_and_permute_players(self, n, rounds_per_game, players, **board_params):
        pass

    def run_n_games_with_all_player_combinations(self, n, rounds_per_game, players, **board_params):
        pass
