from board import Board
from altair import Chart
from pandas import DataFrame

# todo: custom logging levels: turn, round, game
# todo: attatch name to strategy instead of player so only strategy has to be written

class GameManager:
    def __init__(self, players, **board_params):
        self.players = players
        self.board_params = board_params
        self.stats = []

    def run_n_rounds(self, n):
        board = Board(self.players, **self.board_params)
        for _ in range(n):
            board.play_round()
        stats = board.get_stats()
        board.print_end_game_summary()
        self.stats.append(stats)

    def run_n_games(self, n, rounds_per_game=3):
        for _ in range(n):
            self.run_n_rounds(rounds_per_game)

    def run_n_games_and_rotate_players(self, n_games_per_rotation, rounds_per_game=3):
        for n_player in range(len(self.players)):
            self.run_n_games(n_games_per_rotation, rounds_per_game)
            self.players = [self.players.pop()] + self.players
        print('Done!')

    def run_n_games_and_permute_players(self, n, rounds_per_game=3):
        pass

    def run_n_games_with_all_player_combinations(self, n, rounds_per_game=3):
        pass

    def plot_wins(self):
        wins = {}
        for game_stat in self.stats:
            for player_name, player_stat in game_stat.items():
                if player_name not in wins:
                    wins[player_name] = 0
                if player_stat['rank'] == 1:
                    wins[player_name] += 1

        wins_df = DataFrame({
            'Players': list(wins.keys()),
            'Wins': list(wins.values())
        })
        plot = Chart(wins_df).mark_bar().encode(x='Players', y='Wins')
        plot.save('wins.png')
