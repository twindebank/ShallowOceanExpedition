from copy import copy
from unittest.mock import MagicMock, call, patch

from pytest import fixture

from ShallowOceanExpedition.game_manager import GameManager


@fixture
def game_manager():
    gm = GameManager(MagicMock())
    gm._simulation_time = 'time'
    return gm


@patch('ShallowOceanExpedition.game_manager.GameManager.new_board')
def test_GameManager_run_n_rounds(mock_board, game_manager):
    mock_board.get_stats.return_value = 'stat'
    game_manager.run_n_rounds(3)
    assert mock_board.play_round.call_args_list == [call()] * 3
    mock_board.get_stats.assert_called()
    mock_board.print_end_game_summary.assert_called()
    assert game_manager.stats == ['stat']
    assert game_manager.plot_title == 'Time: 3 Rounds'


def test_GameManager_run_n_games(game_manager):
    game_manager.run_n_rounds = MagicMock()
    game_manager.run_n_games(10, rounds_per_game=2)
    assert game_manager.run_n_rounds.call_args_list == [call(2)] * 10
    assert game_manager.plot_title == 'Time: 10 Games, 2 Rounds Per Game'


class MockGameManager(GameManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._simulation_time = 'time'
        self.strategies_used = []

    def run_n_games(self, n, rounds_per_game=3):
        self.strategies_used.append(copy(self.strategies))


def test_GameManager_run_n_games_and_rotate_strategies():
    game_manager = MockGameManager(MagicMock())
    game_manager.strategies = [1, 2, 3, 4]
    game_manager.run_n_games_and_rotate_strategies(10, rounds_per_game=2)

    expected_strategies_used = [
        [1, 2, 3, 4],
        [4, 1, 2, 3],
        [3, 4, 1, 2],
        [2, 3, 4, 1]
    ]
    assert game_manager.strategies_used == expected_strategies_used

    # assert game_manager.run_n_rounds.call_args_list == [call(2)] * 10
    assert game_manager.plot_title == 'Time: Rotated Strategies, 10 Games Per Rotation, 2 Rounds Per Game '


# def test_GameManager_run_n_games_and_permute_strategies():
#     assert False
#
#
# def test_GameManager_run_n_games_with_all_strategy_combinations():
#     assert False


def test_GameManager_aggregate_wins(game_manager):
    mock_stats = [
        {
            'strat1': {
                'rank': 1
            },
            'strat2': {
                'rank': 2
            },
            'strat3': {
                'rank': 3
            }
        },
        {
            'strat1': {
                'rank': 2
            },
            'strat2': {
                'rank': 2
            },
            'strat3': {
                'rank': 1
            }
        },
        {
            'strat1': {
                'rank': 3
            },
            'strat2': {
                'rank': 1
            },
            'strat3': {
                'rank': 2
            }
        },
        {
            'strat1': {
                'rank': 1
            },
            'strat2': {
                'rank': 2
            },
            'strat3': {
                'rank': 3
            }
        }
    ]
    game_manager.stats = mock_stats
    wins = game_manager.aggregate_wins()
    assert wins == {
        'strat1': 2,
        'strat2': 1,
        'strat3': 1
    }
