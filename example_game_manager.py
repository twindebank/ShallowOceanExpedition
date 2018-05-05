from board import Board
from game_manager import GameManager
from player import Player
from strategy import DefaultStrategy


def main():
    players = [
        Player('Theo', DefaultStrategy()),
        Player('Tati', DefaultStrategy())
    ]
    game_manager = GameManager(players)
    game_manager.run_n_games(1)


if __name__ == '__main__':
    main()
