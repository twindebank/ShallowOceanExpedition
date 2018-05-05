from game.game_manager import GameManager
from game.components.strategy import DefaultStrategy


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
    game_manager.run_n_games_and_rotate_players(1000)
    game_manager.plot_wins('wins.png')


if __name__ == '__main__':
    main()
