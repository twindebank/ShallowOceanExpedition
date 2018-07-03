from ShallowOceanExpedition.components.board import Board
from ShallowOceanExpedition.components.strategy import DefaultStrategy
from ShallowOceanExpedition.utils.logging import logger, TURN

logger.setLevel(TURN)


def main():
    strategies = [
        DefaultStrategy('Player1'),
        DefaultStrategy('Player2'),
        DefaultStrategy('Player3'),
        DefaultStrategy('Player4'),
    ]
    board = Board(strategies)
    for _ in range(3):
        board.play_round()
    board.print_end_game_summary()


print('Done!')

if __name__ == '__main__':
    main()
