from game.components.board import Board
from game.components.strategy import DefaultStrategy
from game.utils.logging import logger, TURN

logger.setLevel(TURN)

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
    board = Board(strategies)
    for _ in range(3):
        board.play_round()
    board.print_end_game_summary()


print('Done!')

if __name__ == '__main__':
    main()
