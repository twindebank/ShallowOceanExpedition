from board import Board
from player import Player
from strategy import DefaultStrategy


def main():
    players = [
        Player('Theo', DefaultStrategy()),
        Player('Tati', DefaultStrategy())
    ]
    board = Board(players)
    board.play_n_rounds(3)
    print('Done!')


if __name__ == '__main__':
    main()
