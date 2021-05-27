# This file contains tests for FocusGame.
import unittest
from FocusGame import FocusGame, Tile, Board


class FocusGameTests(unittest.TestCase):
    # write test methods below

    def test_initializer_of_focus_game_creates_object_when_passed_valid_parameters(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertIsInstance(g, FocusGame)

    def test_initializer_of_focus_game_does_not_create_FocusGame_object_when_not_passed_valid_parameters(self):
        def f():
            g = FocusGame()
        self.assertRaises(TypeError, f)

    def test_max_height_initialized_with_FocusGame_object_to_five(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g._max_height, 5)

    def test_turn_assigned_to_first_player_name_in_tuple_in_arguments_when_passed_string_name(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g._turn, g._p1.get_name())

    def test_if_turn_set_to_second_players_name_after_change_turn_passed_player1(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g.change_turn('player1')
        self.assertEqual(g.get_turn(), "player2")

    def test_if_check_turn_returns_false_when_player_name_passed_does_not_match_current_turn(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g.check_turn(g._p2.get_name())
        self.assertFalse(g.check_turn(g._p2.get_name()))

    def test_if_board_initialized_incorrectly_with_valid_FocusGame_initialization(self):
        g = FocusGame(("player1", "r"), ("player2", "t"))
        self.assertNotEqual(g._board.get_board(),
                            [["r", "r", "g", "g", "r", "r"],
                             ["g", "g", "r", "r", "g", "g"],
                             ["r", "r", "g", "g", "r", "r"],
                             ["g", "g", "r", "r", "g", "g"],
                             ["r", "r", "g", "g", "r", "r"],
                             ["g", "g", "r", "r", "g", "g"]],
                            "They are equal.")

    def test_if_tile_init_creates_Tile_when_passed_valid_parameters(self):
        g = Tile((0, 0), ["r"])
        self.assertIsInstance(g, Tile)

    def test_if_get_position_from_Tile_returns_tuple_of_2_numbers_when_passed_valid_parameters(self):
        g = Tile((0, 0), ["r"])
        self.assertEqual((0, 0), g.get_position())

    def test_if_get_pieces_from_Tile_returns_list_of_pieces_when_passed_valid_parameters(self):
        g = Tile((0, 0), ["r", 'g', 'g'])
        self.assertEqual(["r", 'g', 'g'], g.get_pieces())

    def test_get_tile_returns_tile_object_at_valid_coordinates_passed_to_get_tile(self):
        g = FocusGame(('player1', 'r',), ('player2', 'g'))
        self.assertIsInstance(g._board.get_tile((0, 0)), Tile)

    def test_if_get_height_from_Tile_returns_number_of_pieces_in_Tile_pieces(self):
        g = Tile((0, 0), ["r", 'g', 'g'])
        self.assertEqual(3, g.get_height())

    def test_if_get_top_from_Tile_returns_piece_colour_on_top_of_Tile_pieces(self):
        g = Tile((0, 0), ["r", 'g', 'g'])
        self.assertEqual('g', g.get_top())

    def test_check_location_passing_valid_parameters(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.check_location(1, (0, 0), (1, 0)), True)

    def test_check_location_passing_invalid_parameters(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.check_location(1, (0, 1), (0, 0)), True)

    def test_check_number_of_pieces_passing_valid_number_of_pieces(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.check_number_of_pieces(1, (0, 0)), True)

    def test_check_number_of_pieces_passing_too_many_pieces(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.check_number_of_pieces(2, (0, 0)), False)

    def test_get_tile_location_with_valid_location(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(type(g.get_tile((0, 0))), Tile)

    def test_show_reserve_with_invalid_name(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.show_reserve("Player"), False)

    def test_show_reserve_with_valid_name_and_0_in_reserve(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.show_reserve("player2"), 0)

    def test_change_reserves_and_reserved_move_passing_invalid_name(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        self.assertEqual(g.reserved_move('player', (1, 1)), False)

    def test_reserved_move_passing_invalid_location_off_board(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        self.assertEqual(g.reserved_move('player1', (1, 6)), False)

    def test_reserved_move_on_wrong_turn(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        self.assertEqual(g.reserved_move('player2', (1, 1)), False)

    def test_reserved_move_passing_invalid_number_of_reserves(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.reserved_move('player1', (1, 1)), False)

    def test_reserved_move_passing_valid_parameters_does_not_make_tile_height_more_than_5_adds_new_colour_to_tile(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        g.reserved_move('player1', (1, 1))
        self.assertEqual(g.get_tile((1, 1)).get_pieces(), ['g', 'r'])

    def test_reserved_move_passing_valid_parameters_changes_tile_pieces_accordingly(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        g.reserved_move('player1', (1, 1))
        self.assertEqual(g.get_tile((1, 1)).get_pieces(), ['g', 'r'])

    def test_reserved_move_passing_valid_parameters_changes_reserves_count_accordingly(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        g.reserved_move('player1', (1, 1))
        self.assertEqual(g.show_reserve('player1'), 4)

    def test_reserved_move_passing_valid_parameters_changes_turn_accordingly(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        g.reserved_move('player1', (1, 1))
        self.assertEqual(g.get_turn(), 'player2')

    def test_check_win_passing_player_with_over_6_captured(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g._p1.change_reserves(5)
        g._p1.change_captured(7)
        g.check_win('player1')
        self.assertEqual(g.check_win('player1'), True)

    def test_show_pieces_passing_valid_tile_position(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.show_pieces((0, 0)), ['r'])

    def test_get_player_from_name_passing_invalid_name(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.get_player_from_name("player"), False)

    def test_move_piece_on_wrong_turn(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player2', (0, 0), (1, 0), 1), False)

    def test_move_piece_on_correct_turn(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (1, 0), 1), 'successfully moved')

    def test_move_piece_passing_invalid_name(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player', (0, 0), (1, 0), 1), False)

    def test_move_piece_passing_invalid_destination_off_board(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (1, 6), 1), False)

    def test_move_piece_passing_invalid_start_off_board(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, -1), (0, 1), 1), False)

    def test_move_piece_with_invalid_starting_tile_because_wrong_pile_top(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (1, 0), (1, 1), 1), False)

    def test_move_piece_passing_same_destination_as_start(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (0, 0), 1), False)

    def test_move_piece_passing_destination_at_diagonal_from_start(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (1, 1), 1), False)

    def test_move_piece_passing_too_many_pieces_to_move(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (3, 0), 3), False)

    def test_move_piece_passing_valid_destination(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (1, 0), 1), 'successfully moved')

    def test_move_piece_passing_valid_start(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        self.assertEqual(g.move_piece('player1', (0, 0), (1, 0), 1), 'successfully moved')

    def test_multiple_move_passing_valid_parameters_moving_3_pieces(self):
        g = FocusGame(("player1", "r"), ("player2", "g"))
        g.move_piece('player1', (0, 0), (0, 1), 1)
        g.move_piece('player2', (1, 0), (1, 1), 1)
        g.move_piece('player1', (0, 1), (0, 3), 2)
        g.move_piece('player2', (1, 1), (1, 3), 2)
        g.move_piece('player1', (0, 3), (1, 3), 1)
        self.assertEqual(g.get_tile((1, 3)).get_pieces(), ['r', 'g', 'g', 'r'])


if '__name__' == "__main__":
    # provided test
    unittest.main()
