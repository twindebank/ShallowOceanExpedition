from ShallowOceanExpedition.game_manager import GameManager
from ShallowOceanExpedition.components.strategy import DefaultStrategy
from ShallowOceanExpedition.utils.logging import logger, SIM

logger.setLevel(SIM)

def main():
    strategies = [
        DefaultStrategy('Theo'),
        DefaultStrategy('Tati'),
        DefaultStrategy('Jon'),
        DefaultStrategy('Gabriel'),
        DefaultStrategy('Alastair'),
        DefaultStrategy('Maria'),
        DefaultStrategy('Lisa'),
    ]
    game_manager = GameManager(strategies)
    game_manager.run_n_games_and_rotate_strategies(10000)
    game_manager.plot_wins('wins.png')


if __name__ == '__main__':
    main()
