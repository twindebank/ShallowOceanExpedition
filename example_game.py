from board import Board
from exceptions import RoundOver
from player import Player
from strategy import DefaultStrategy


def main():
    players = [
        Player('Theo', DefaultStrategy()),
        Player('Tati', DefaultStrategy())
    ]
    board = Board(players)
    play_round(board)
    play_round(board)
    play_round(board)
    board.end_game_summary()
    print('Done!')


def play_round(board):
    while board.has_players():
        try:
            board.take_turn()
        except RoundOver:
            break


if __name__ == '__main__':
    main()
