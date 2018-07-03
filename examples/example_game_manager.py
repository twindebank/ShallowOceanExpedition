from ShallowOceanExpedition.game_manager import GameManager
from ShallowOceanExpedition.components.strategy import DefaultStrategy
from ShallowOceanExpedition.utils.logging import logger, SIM

logger.setLevel(SIM)


def main():
    strategies = [
        DefaultStrategy('Player1'),
        DefaultStrategy('Player2'),
        DefaultStrategy('Player3'),
        DefaultStrategy('Player4')
    ]
    game_manager = GameManager(strategies)
    game_manager.run_n_games_and_rotate_strategies(10000)
    game_manager.plot_wins('wins.png')


if __name__ == '__main__':
    main()
