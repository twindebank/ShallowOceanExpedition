from tqdm import tqdm

from ShallowOceanExpedition.components.board import Board
from ShallowOceanExpedition.utils.logging import logger, SIM
from ShallowOceanExpedition.utils.pretty_plot import PrettyPlot
from datetime import datetime


class GameManager:
    def __init__(self, strategies, **board_params):
        self.strategies = strategies
        self.board_params = board_params
        self.stats = []  # list of stats PER ROUND
        self._simulation_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self._plot_title = None

    def run_n_rounds(self, n):
        board = Board(self.strategies, **self.board_params)
        for _ in range(n):
            board.play_round()
        stats = board.get_stats()
        board.print_end_game_summary()
        board.hard_reset_players()
        self.stats.append(stats)
        self.plot_title = f'{n} rounds'

    def run_n_games(self, n, rounds_per_game=3):
        n_games_iter = tqdm(range(n)) if logger.level == SIM else range(n)
        for _ in n_games_iter:
            self.run_n_rounds(rounds_per_game)
        self.plot_title = f'{n} games, {rounds_per_game} rounds per game'

    def run_n_games_and_rotate_strategies(self, n_games_per_rotation, rounds_per_game=3):
        logger.log(SIM, f'Running {n_games_per_rotation} games...')
        for n_strategy in range(len(self.strategies)):
            self.run_n_games(n_games_per_rotation, rounds_per_game)
            self.strategies = [self.strategies.pop()] + self.strategies
        self.plot_title = f"rotated strategies, {n_games_per_rotation} games per rotation, {rounds_per_game} rounds " \
                          f"per game "

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

        plot = PrettyPlot()
        plot.add_bar_chart(
            list(wins.values()),
            list(wins.keys()),
            x_axis_label='Strategies',
            y_axis_label='Wins',
            title=self.plot_title
        )
        logger.log(SIM, f'Saving plot to file "{save_path}"')
        plot.save_fig(save_path)

    @property
    def plot_title(self):
        return self._plot_title.title()

    @plot_title.setter
    def plot_title(self, title):
        self._plot_title = f'{self._simulation_time}: {title}'
