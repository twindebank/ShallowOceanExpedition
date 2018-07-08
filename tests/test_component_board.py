from copy import copy
from unittest.mock import patch, MagicMock

import pytest

from ShallowOceanExpedition.components.board import Board
from ShallowOceanExpedition.components.tiles import Home, BlankTile, Tile
from ShallowOceanExpedition.utils.exceptions import RoundOver, Cheating


@pytest.fixture
def board():
    return Board([MockStrategy('1'), MockStrategy('2')])


@pytest.fixture
def board_4p():
    return Board([MockStrategy('1'), MockStrategy('2'), MockStrategy('3'), MockStrategy('4')])


class MockStrategy:
    def __init__(self, name):
        self.player_name = name


class MockTile:
    def __init__(self, level):
        self.level = level if level is None else tuple([level])


def test_Board_init(board):
    with pytest.raises(ValueError):
        Board([])
    with pytest.raises(ValueError):
        Board([MockStrategy('test')])

    assert [player.name for player in board.players] == ['1', '2']

    assert isinstance(board.tiles[0], Home)
    tile_levels = [tile.level for tile in board.tiles[1:]]
    expected_tile_levels = [
        (1,), (1,), (1,), (1,), (1,),
        (2,), (2,), (2,), (2,), (2,),
        (3,), (3,), (3,), (3,), (3,),
        (4,), (4,), (4,), (4,), (4,)
    ]
    assert tile_levels == expected_tile_levels
    assert board.round_number == 0
    assert board.oxygen == board.original_oxygen == 25
    assert board.current_player.name == '1'


@patch('ShallowOceanExpedition.components.board.Board._take_turn', side_effect=RoundOver)
def test_Board_play_round(board):
    board.play_round()


@patch('ShallowOceanExpedition.components.board.Board._reduce_ox_by')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_direction_strategy')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_drop_strategy')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_collect_strategy')
@patch('ShallowOceanExpedition.components.board.Board._advance_current_player')
@patch('ShallowOceanExpedition.components.board.Board._has_players')
@patch('ShallowOceanExpedition.components.board.Board._end_round')
@patch('ShallowOceanExpedition.components.board.Board._next_player')
def test_Board_take_turn_land_on_tile(next_player, end_round, has_players, advance_player, collect_strategy,
                                      drop_strategy, direction_strategy, reduce_ox, board):
    advance_player.return_value = MockTile(1)
    board._take_turn()
    assert has_players.called
    assert reduce_ox.called
    assert direction_strategy.called
    assert not drop_strategy.called
    assert collect_strategy.called
    assert next_player.called


@patch('ShallowOceanExpedition.components.board.Board._reduce_ox_by')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_direction_strategy')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_drop_strategy')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_collect_strategy')
@patch('ShallowOceanExpedition.components.board.Board._advance_current_player')
@patch('ShallowOceanExpedition.components.board.Board._has_players')
@patch('ShallowOceanExpedition.components.board.Board._end_round')
@patch('ShallowOceanExpedition.components.board.Board._next_player')
def test_Board_take_turn_land_on_home(next_player, end_round, has_players, advance_player, collect_strategy,
                                      drop_strategy, direction_strategy, reduce_ox, board):
    board.current_player = MagicMock()
    board.current_player.back_home = False
    advance_player.return_value = Home()
    board._take_turn()
    assert has_players.called
    assert reduce_ox.called
    assert direction_strategy.called
    assert board.current_player.reached_home.called
    assert not drop_strategy.called
    assert not collect_strategy.called
    assert next_player.called

    board.current_player.reached_home.return_value = True
    board._has_players.return_value = False
    board._take_turn()
    assert board._end_round.called


@patch('ShallowOceanExpedition.components.board.Board._reduce_ox_by')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_direction_strategy')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_drop_strategy')
@patch('ShallowOceanExpedition.components.board.Board._apply_current_player_collect_strategy')
@patch('ShallowOceanExpedition.components.board.Board._advance_current_player')
@patch('ShallowOceanExpedition.components.board.Board._has_players')
@patch('ShallowOceanExpedition.components.board.Board._end_round')
@patch('ShallowOceanExpedition.components.board.Board._next_player')
def test_Board_take_turn_land_on_blank(next_player, end_round, has_players, advance_player, collect_strategy,
                                       drop_strategy, direction_strategy, reduce_ox, board):
    blank = MockTile(None)
    advance_player.return_value = blank
    board._take_turn()
    assert has_players.called
    assert reduce_ox.called
    assert direction_strategy.called
    assert drop_strategy.called
    assert not collect_strategy.called
    assert next_player.called


@patch('ShallowOceanExpedition.components.board.Board._end_round')
def test_Board_take_turn_oxygen_depleted(end_round, board):
    board.oxygen = 0
    board._take_turn()
    assert end_round.caled


def test_Board_has_players(board):
    assert board._has_players()

    board.players[0].back_home = True
    board.players[1].back_home = True

    assert not board._has_players()


def test_Board_summarise_tile_levels(board):
    expected_tile_levels = [
        'Home',
        (1,), (1,), (1,), (1,), (1,),
        (2,), (2,), (2,), (2,), (2,),
        (3,), (3,), (3,), (3,), (3,),
        (4,), (4,), (4,), (4,), (4,)
    ]

    assert board._summarise_tile_levels() == expected_tile_levels


def test_Board_apply_current_player_collect_strategy_pickup(board):
    board.current_player.strategy = MagicMock()
    board.current_player.strategy.tile_collect.return_value = True
    board.current_player.collect_tile = MagicMock()
    first_tile = board.tiles[1]
    # try to pick up home
    with pytest.raises(Cheating):
        board._apply_current_player_collect_strategy()

    # pick up tile
    board.current_player.position = 1
    board._apply_current_player_collect_strategy()
    board.current_player.collect_tile.assert_called_with(first_tile)
    assert isinstance(board.tiles[1], BlankTile)

    # try to pick up blank tile
    with pytest.raises(Cheating):
        board._apply_current_player_collect_strategy()


def test_Board_apply_current_player_collect_strategy_dont_pickup(board):
    board.current_player.strategy = MagicMock()
    board.current_player.collect_tile = MagicMock()
    tiles = copy(board.tiles)
    board.current_player.strategy.tile_collect.return_value = False
    assert board.tiles == tiles
    assert not board.current_player.collect_tile.called


def test_Board_apply_current_player_drop_strategy_do_drop(board):
    board.current_player.strategy = MagicMock()
    player_tiles = [Tile(1), Tile(1), Tile(2)]
    board.current_player.tiles = list(player_tiles)
    board.current_player.strategy.tile_drop.return_value = (True, (1,))
    # try to drop on home
    with pytest.raises(Cheating):
        board._apply_current_player_drop_strategy()

    # drop on blank tile
    board.current_player.position = 1
    board.tiles[1] = BlankTile()
    board._apply_current_player_drop_strategy()
    assert isinstance(board.tiles[1], Tile)
    assert board.tiles[1].level == (1,)
    assert board.current_player.tiles == player_tiles[1:]

    # try to drop on existing tile
    with pytest.raises(Cheating):
        board._apply_current_player_drop_strategy()


def test_Board_apply_current_player_drop_strategy_dont_drop(board):
    board.current_player.strategy = MagicMock()
    board.current_player.drop_tile = MagicMock()
    board.current_player.strategy.tile_drop.return_value = (False, None)
    board._apply_current_player_drop_strategy()
    assert not board.current_player.drop_tile.called


def test_Board_apply_current_player_direction_strategy(board):
    board.current_player.strategy = MagicMock()
    board.current_player.strategy.decide_direction.return_value = True
    assert board.current_player.direction == 1

    board._apply_current_player_direction_strategy()
    assert board.current_player.direction == -1

    with pytest.raises(Cheating):
        board._apply_current_player_direction_strategy()

    board.current_player.strategy.decide_direction.return_value = False
    board._apply_current_player_direction_strategy()


@patch('ShallowOceanExpedition.components.board.Board._calculate_new_position')
def test_Board_advance_current_player(new_pos, board):
    assert board.current_player.position == 0
    assert board.current_player.n_turn == 0

    new_pos.return_value = 2
    landed_on = board._advance_current_player()
    assert board.current_player.position == 2
    assert board.current_player.n_turn == 1
    assert landed_on.level == (1,)


@patch('ShallowOceanExpedition.components.board.Player.roll')
def test_Board_calculate_new_position_no_tiles(roll, board_4p):
    assert board_4p.current_player.position == 0

    # no players in front
    board_4p.players[0].position = 0
    board_4p.players[1].position = 0
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 5
    new = board_4p._calculate_new_position()
    assert new == 5

    # one player in front within roll distance
    board_4p.players[0].position = 0
    board_4p.players[1].position = 1
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 5
    new = board_4p._calculate_new_position()
    assert new == 6

    # two players in front one within roll distance
    board_4p.players[0].position = 0
    board_4p.players[1].position = 1
    board_4p.players[2].position = 7
    board_4p.players[3].position = 0
    roll.return_value = 5
    new = board_4p._calculate_new_position()
    assert new == 6

    # two players in front both within roll distance
    board_4p.players[0].position = 0
    board_4p.players[1].position = 1
    board_4p.players[2].position = 5
    board_4p.players[3].position = 0
    roll.return_value = 5
    new = board_4p._calculate_new_position()
    assert new == 7

    # two in front and one behind
    board_4p.players[0].position = 3
    board_4p.players[1].position = 1
    board_4p.players[2].position = 4
    board_4p.players[3].position = 5
    roll.return_value = 5
    new = board_4p._calculate_new_position()
    assert new == 10

    # beyond board
    board_4p.players[0].position = 15
    board_4p.players[1].position = 0
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 200
    new = board_4p._calculate_new_position()
    assert new == len(board_4p.tiles) - 1

    # roll none
    board_4p.players[0].position = 10
    board_4p.players[1].position = 0
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 0
    new = board_4p._calculate_new_position()
    assert new == 10

    # backward none in roll distance
    board_4p.players[0].direction = -1
    board_4p.players[0].position = 5
    board_4p.players[1].position = 0
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 3
    new = board_4p._calculate_new_position()
    assert new == 2

    # backwards one in roll distance
    board_4p.players[0].direction = -1
    board_4p.players[0].position = 5
    board_4p.players[1].position = 3
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 3
    new = board_4p._calculate_new_position()
    assert new == 1

    # backwards one in roll distance one not
    board_4p.players[0].direction = -1
    board_4p.players[1].position = 5
    board_4p.players[1].position = 4
    board_4p.players[2].position = 0
    board_4p.players[3].position = 1
    roll.return_value = 2
    new = board_4p._calculate_new_position()
    assert new == 2

    # backwards both in roll distance
    board_4p.players[0].direction = -1
    board_4p.players[0].position = 5
    board_4p.players[1].position = 2
    board_4p.players[2].position = 1
    board_4p.players[3].position = 0
    roll.return_value = 3
    new = board_4p._calculate_new_position()
    assert new == 0

    # backwards two in distance one in front
    board_4p.players[0].direction = -1
    board_4p.players[0].position = 5
    board_4p.players[1].position = 4
    board_4p.players[2].position = 1
    board_4p.players[3].position = 6
    roll.return_value = 3
    new = board_4p._calculate_new_position()
    assert new == 0

    # backwards beyond home
    board_4p.players[0].direction = -1
    board_4p.players[0].position = 5
    board_4p.players[1].position = 0
    board_4p.players[2].position = 0
    board_4p.players[3].position = 0
    roll.return_value = 200
    new = board_4p._calculate_new_position()
    assert new == 0


def test_Board_get_other_player_positions(board_4p):
    assert board_4p._get_other_player_positions() == [0, 0, 0]

    board_4p.players[0].position = 1
    assert board_4p._get_other_player_positions() == [0, 0, 0]

    board_4p.players[0].position = 1
    board_4p.players[1].position = 2
    assert board_4p._get_other_player_positions() == [2, 0, 0]

    board_4p.players[0].position = 1
    board_4p.players[1].position = 2
    board_4p.players[2].position = 3
    board_4p.players[3].position = 4
    assert board_4p._get_other_player_positions() == [2, 3, 4]


def test_Board_get_other_players(board_4p):
    other_players = board_4p._get_other_players()
    assert [player.name for player in other_players] == ['2', '3', '4']


def test_Board_next_player(board_4p):
    players = board_4p.players
    assert board_4p.current_player == players[0]

    board_4p._next_player()
    assert board_4p.current_player == players[1]

    board_4p._next_player()
    assert board_4p.current_player == players[2]

    board_4p._next_player()
    assert board_4p.current_player == players[3]

    board_4p._next_player()
    assert board_4p.current_player == players[0]


@patch('ShallowOceanExpedition.components.board.Board._end_round')
def test_Board_reduce_ox_by(end_round, board):
    assert board.oxygen == 25

    board._reduce_ox_by(5)
    assert board.oxygen == 20

