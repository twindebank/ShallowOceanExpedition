from game.components.board import Board
from altair import Chart
from pandas import DataFrame
from tqdm import tqdm

from game.utils.logging import logger, SIM


class GameManager:
    def __init__(self, strategies, **board_params):
        self.strategies = strategies
        self.board_params = board_params
        self.stats = []

    def run_n_rounds(self, n):
        board = Board(self.strategies, **self.board_params)
        for _ in range(n):
            board.play_round()
        stats = board.get_stats()
        board.print_end_game_summary()
        board.hard_reset_players()
        self.stats.append(stats)

    def run_n_games(self, n, rounds_per_game=3):
        iter = tqdm(range(n)) if logger.level == SIM else range(n)
        for _ in iter:
            self.run_n_rounds(rounds_per_game)

    def run_n_games_and_rotate_strategies(self, n_games_per_rotation, rounds_per_game=3):
        logger.log(SIM, f'Running {n_games_per_rotation} games...')
        for n_strategy in range(len(self.strategies)):
            self.run_n_games(n_games_per_rotation, rounds_per_game)
            self.strategies = [self.strategies.pop()] + self.strategies

    def run_n_games_and_permute_strategies(self, n, rounds_per_game=3):
        pass

    def run_n_games_with_all_strategy_combinations(self, n, rounds_per_game=3):
        pass

    def plot_wins(self, save_path):
        logger.log(SIM, 'Plotting wins...')
        wins = {}
        for game_stat in self.stats:
            for strategy_name, strategy_stat in game_stat.items():
                if strategy_name not in wins:
                    wins[strategy_name] = 0
                if strategy_stat['rank'] == 1:
                    wins[strategy_name] += 1

        wins_df = DataFrame({
            'strategies': list(wins.keys()),
            'Wins': list(wins.values())
        })
        plot = Chart(wins_df).mark_bar().encode(x='strategies', y='Wins')
        logger.log(SIM, f'Saving plot to file "{save_path}"')
        plot.save(save_path)
