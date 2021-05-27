# Author: Omar Fakhreddine
# Date: 11/25/2020
# Description:
"""
This Program is used to play the game Domination. This will allow 2 players to
play the game, they decide who can start. The player has 3 options on their
turn, single move, multiple move, reserve/capture & reserve move. The game ends
 when one player captures 6 pieces.
"""


class FocusGame:
    """
    FocusGame represents an object that contains init (needing 2 tuples with
    player name and colour) and methods: move_piece, shoe_pieces, show_reserve,
    show_captured, initialize_board and reserved_move
    It communicates with Player when obtaining information about their name,
    colour, reserves, and captures
    It communicates with Stack when obtaining information about what exists
    on each tile of the initialized board, and also used to fill each tile
    with Stack objects

    move_piece: takes player name, tuple of coordinates for where move starts,
    tuple for target location, integer for # of pieces being moved. Returns
    error message if, out of turn move, invalid locations or invalid # of pieces.
    Returns message if move successful or player wins.

    show_pieces: takes position and returns list of pieces(bottom at list[0]

    show_reserve: takes player name and shows count of reserved pieces, if none, return 0

    show_captured: takes player name and shows # of pieces captured, if none, return 0

    reserved_move: takes player name & location on board. Places reserved
    piece at location(appends to list), reduce reserve piece by 1, if no pieces
    in reserve, return "no pieces in reserve"
    """

    def __init__(self, p1, p2):
        """
        initializes the 2 players' names and colours by taking 2 tuples
        (1 for each player) and then initializing the board to desired size(6x6 default)
        positions where each position has a piece marked R or G for red and green
        respectively. p1/p2: tuple where first item is their name(str) and second is their
        colour(str). Example tuple ("PlayerA", "G")
        """
        self._p1 = Player(p1)
        self._p2 = Player(p2)
        self._board = Board(self._p1.get_colour(), self._p2.get_colour())
        self._max_height = 5
        self._turn = self._p1.get_name()

    def move_piece(self, name, start, destination, num_of_pieces):
        """
        checks if name is == to _turn using check_turn.
        checks if name is valid and one of p1 or p2 names
        checks if the move is valid using check_location, where the start, destination
        and num_of_pieces are communicated with check_location.
        checks if pieces trying to be moved at location start are valid using check_pieces

        find destination tile in board using Board.get_tile, save pieces to
        Tile._pieces at destination by passing a var with the list of pieces to
        Tile.add while tile height > 5, tile.remove_piece, check return value if
        p1 colour or p2 colour, add1 to reserve or captures accordingly.
        If no errors and piece(s) successfully moved, print "successfully moved."
        If move returns True from self.check_win, print(<name> + " Wins").
        Call change_turn to update who's turn it is.
        :param name: players name (str)
        :param start: tuple of coordinates of piece location to move
        :param destination: tuple of coordinates of destination to move
        :param num_of_pieces: int of # of pieces to move
        :return: changes Tile object in board, potentially _captures/_reserves of player
                 prints "successfully moved" or <name> wins, changes turn, or errors
        """
        player = self.get_player_from_name(name)
        if not player:
            return False
        elif not self.check_turn(name):
            return False
        elif not self.check_location(num_of_pieces, start, destination):
            return False
        elif not self.check_number_of_pieces(num_of_pieces, start):
            return False
        else:
            start_tile = self.get_tile(start)
            end_tile = self.get_tile(destination)
            pile = start_tile.get_pieces()[len(
                start_tile.get_pieces())-num_of_pieces:]

            end_tile.add(pile)
            for _ in range(num_of_pieces):
                self.change_reserves_captured(player, destination)
                start_tile.remove_top()
            print("successfully moved")
            if self.check_win(name):
                print(name + " wins!")
                return name + " wins!"
            self.change_turn(name)
            return "successfully moved"

    def show_pieces(self, position):
        """
        takes position(tuple) and returns list of pieces(bottom at list[0]) from Tile
        object using Board.get_tile and Tile.get_pieces
        :param position: tuple coordinates
        :return: list of pieces
        """
        if not self.check_on_board(position):
            return False
        else:
            return self._board.get_tile(position).get_pieces()

    def show_reserve(self, name):
        """
        check if player exists first then return Player.reserves using get_player
        _form_name showing count of reserved pieces
        :param name: string of player's name
        :return: int of player reserves
        """
        player = self.get_player_from_name(name)
        if player is False:
            return False
        else:
            return player.get_reserves()

    def show_captured(self, name):
        """
        check if player exists and find player using get_player_from_name first then
        return Player.captured showing # of pieces captured
        :param name: str of name
        :return: int of captured pieces
        """
        player = self.get_player_from_name(name)
        if player is False:
            return False
        else:
            return player.get_captures()

    def reserved_move(self, name, location):
        """
        uses player name and get_player to get player Object, then check_reserves(name)
        to determine if any pieces in reserve, if >= 1, places reserved piece at
        location(extends Tile._pieces), decrement reserve piece by 1 and change
        turn to other player, if no pieces in reserve, return "no pieces in reserve"
        :param name: string of player name
        :param location: coordinates tuple of location to place reserve
        :return: "no pieces in reserve" or changes Tile._pieces at Board.get_tile(location)
                 and decrements player._reserves
        """
        player = self.get_player_from_name(name)
        if not player:
            return False
        elif not self.check_turn(name):
            return False
        elif not self.check_reserves(name):
            return False
        elif not self.check_on_board(location):
            return False
        else:
            self.get_tile(location).add([player.get_colour()])
            player.change_reserves(-1)
            self.change_reserves_captured(player, location)
            print("successfully moved")
            if self.check_win(name):
                print(name + " wins!")
                return name + " wins!"
            self.change_turn(name)
            return "successfully moved"

    def get_p1(self):
        # returns player 1
        return self._p1

    def get_p2(self):
        # returns player 2
        return self._p2

    def get_turn(self):
        # returns turn
        return self._turn

    def get_tile(self, tile_location):
        # returns Tile at tile_location in _board
        return self._board.get_tile(tile_location)

    def get_board(self):
        # returns board of Tiles
        return self._board

    def get_player_from_name(self, name):
        # returns Player object from name
        if self._p1.get_name() == name:
            return self._p1
        elif self._p2.get_name() == name:
            return self._p2
        else:
            return False

    def change_turn(self, name):
        """
        yield other player that is not player passed to this method(next player's turn)
        :param name: string name for player currently playing
        :return: change value of FocusGame._turn and
        """
        if name == self._p1.get_name():
            self._turn = self._p2.get_name()
        else:
            self._turn = self._p1.get_name()

    def check_turn(self, name):
        """
        checks if _turn and current and player are the same, if so, return True, if
        not, return False, if turn_num = 0,
        :param name: name of player doing move
        :return: True or False
        """
        if name != self._turn:
            return False
        else:
            return True

    def check_number_of_pieces(self, num_of_pieces, tile_location):
        """
        check if num_of_pieces == _board.get_tile._height, if > tile height, or
        num_of_pieces == 0, return false
        :param num_of_pieces: integer of num_of_pieces
        :param tile_location: coordinates tuple of tile location to move from
        :return: True or "Invalid number of pieces"
        """
        if num_of_pieces == 0:
            return False
        elif num_of_pieces > self._board.get_tile(tile_location).get_height():
            return False
        else:
            return True

    def check_reserves(self, name):
        """
        checks to see if player belonging to name has reserves to play on reserve move
        :return: True if reserve of name > 0, False otherwise
        """
        if self.get_player_from_name(name).get_reserves() < 1:
            return False
        else:
            return True

    def check_location(self, n_o_p, start, destination):
        """
        check if Board.get_tile(location) returns True if: Tile type, if location is
        between (0,0) and (5,5), if location is on same row or column tuple[0] or
        tuple[1] is same for both , if difference in location on row/column < n_o_p
        if not: return False
        :param n_o_p: number of pieces to be moved, int
        :param start: coordinates tuple of Tile to be moved from
        :param destination: coordinates tuple of Tile to be moved to
        :return: True or False
        """
        if not self.check_on_board(start):
            return False
        elif not self.check_on_board(destination):
            return False
        elif start == destination:
            return False
        elif start[0] != destination[0] and start[1] != destination[1]:
            return False
        elif abs(destination[0] - start[0]) != n_o_p and \
                abs(destination[1] - start[1]) != n_o_p:
            return False
        elif self.get_tile(start).get_top() != \
                self.get_player_from_name(self._turn).get_colour():
            return False
        else:
            return True

    def check_on_board(self, position):
        """
        checks for check_location if position is on the board
        :param position: tuple of 2 ints, representing row/column respectively
        :return: False if location off board, True otherwise
        """
        if position[0] not in range(self._board.get_length()):
            return False
        elif position[1] not in range(self._board.get_length()):
            return False
        else:
            return True

    def check_win(self, name):
        # check if name.get_captures
        # :param name: string of player's name
        # :return: True if player belonging to name has 6 or more captures, False otherwise
        if self.get_player_from_name(name).get_captures() >= 6:
            return True
        else:
            return False

    def display_board(self):
        # prints out board to help with visualizing the game
        colour_list = []
        for line in self._board.get_board():
            new_line = []
            for tile in line:
                new_line.append(tile.get_pieces())
            colour_list.append(new_line)
        for r in colour_list:
            print(r)
        return colour_list

    def change_reserves_captured(self, player, destination):
        """
        removes pieces from tile with too many pieces and changes reserves and
        captured accordingly
        :param player: player object
        :param destination: tuple coordinates of tile
        :return: changed values of player._reserves/_captured
        """
        if self.get_tile(destination).get_height() > self._max_height:
            if self.get_tile(destination).remove_bottom() == player.get_colour():
                player.change_reserves(1)
            else:
                player.change_captured(1)


class Player:
    """
    Represents a Player object that contains data members: name, colour, reserve,
    captured as data.
    Communicates with FocusGame to provide player data (most importantly reserves and
    captured when determining win condition satisfaction and reserve(d_move).
    """

    def __init__(self, name_colour):
        # initializes player name, colour, reserves(count) and captured(count)
        self._name = name_colour[0]
        self._colour = name_colour[1]
        self._reserves = 0
        self._captured = 0

    def get_name(self):
        # returns name
        return self._name

    def get_colour(self):
        # returns colour
        return self._colour

    def get_reserves(self):
        # returns # of reserves, used by FocusGame.show_reserve and .reserved_move
        return self._reserves

    def get_captures(self):
        # returns # of captures, incremented when a piece is captured, used by
        # FocusGame to determine satisfaction of win condition
        return self._captured

    def change_reserves(self, num):
        # adds num to _reserves
        self._reserves += num

    def change_captured(self, num):
        # adds num to _captures
        self._captured += num


class Board:
    """
    Represents a board object that contains data members length(length of sides)
    and board. Communicates with FocusGame to provide a board to use and uses
    get_stack to provide stack object at provided location.
    Communicates with Stack to initialize each tile with a Stack object representing
    what exists on each tile.
    """

    def __init__(self, p1_colour, p2_colour):
        # initializes the board with data members sides and tiles
        self._length = 6
        self._board_list = []
        self.initialize_board(p1_colour, p2_colour)

    def get_length(self):
        return self._length

    def initialize_board(self, p1_colour, p2_colour):
        """
        Initializes and returns board for FocusGame using the length of the sides
        in _length. Using nested for loops and _length as their range, it makes a
        list of lists where each inner list is a row and each element is a tile.
        """
        def tile_gen():
            while True:
                yield [p1_colour]
                yield [p1_colour]
                yield [p2_colour]
                yield [p2_colour]
        colour = tile_gen()
        initial_board = []

        def rows(r):
            line = []
            for column in range(self._length):
                line.append(Tile((r, column), next(colour)))
            return line

        for row in range(self._length):
            initial_board.append(rows(row))
        self._board_list = initial_board

    def get_tile(self, location):
        """
        returns Tile object by using location coordinates as indexes for row
        and column in the board.
        :param location: tuple of coordinates
        :return: Tile object
        """
        return self._board_list[location[0]][location[1]]

    def get_board(self):
        # returns board of Tiles
        return self._board_list


class Tile:
    """
    Represents Tile object that contain data members: position, top, height, pieces.
    Communicates with Board and FocusGame to provide information on what pieces exist at
    a location using get_pieces, the height using get_height, top of stack using
    get_top and pieces on the Tile using get_pieces
    Pieces is a list of "R" or "G" representing a stack/piece on a tile
    """

    def __init__(self, position, pieces):
        """
        initializes tile position, top, height and pieces
        :param position: tuple of 2 numbers, (row and column)
        :param pieces: list of _p1/_p2._colour
        :return: Tile object
        """
        self._position = position
        self._pieces = pieces
        self._height = len(pieces)
        self._top = self._pieces[-1]

    def get_position(self):
        # returns position
        return self._position

    def get_pieces(self):
        # returns pieces
        return self._pieces

    def get_height(self):
        # returns height
        return self._height

    def get_top(self):
        # returns top
        return self._top

    def add(self, pieces):
        """
        adds list of pieces onto self._pieces by appending to _pieces
        :param pieces: list of str "colour1" or "colour2"
        :return: pieces appended onto Tile._pieces
        """
        self._height += len(pieces)
        self._pieces.extend(pieces)
        self._top = self._pieces[-1]

    def remove_bottom(self):
        """
        removes first element and return it's value
        :return: value of element[0] removed from _pieces
        """
        self._height -= 1
        piece = self._pieces[0]
        del self._pieces[0]
        return piece

    def remove_top(self):
        """
        removes last element/top
        :return: changed value of tile._pieces
        """
        self._height -= 1
        del self._pieces[-1]
        if self._height > 0:
            self._top = self._pieces[-1]


if __name__ == "__main__":
    game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
    game.move_piece('PlayerA', (0, 0), (0, 1), 1)
    game.move_piece('PlayerB', (1, 0), (1, 1), 1)
    game.move_piece('PlayerA', (0, 1), (0, 3), 2)
    game.move_piece('PlayerB', (1, 1), (1, 3), 2)
    print(game.move_piece('PlayerA', (0, 3), (1, 3), 1))
    game.display_board()
