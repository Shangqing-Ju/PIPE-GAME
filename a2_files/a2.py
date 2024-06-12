EMPTY_TILE = "tile"
START_PIPE = "start"
END_PIPE = "end"
LOCKED_TILE = "locked"

SPECIAL_TILES = {
    "S": START_PIPE,
    "E": END_PIPE,
    "L": LOCKED_TILE
}

PIPES = {
    "ST": "straight",
    "CO": "corner",
    "CR": "cross",
    "JT": "junction-t",
    "DI": "diagonals",
    "OU": "over-under"
}

DIRECTION = ['E', 'S', 'W', 'N']


class PipeGame:
    """
    A game of Pipes.
    """

    def __init__(self, game_file='game_1.csv'):
        """
        Construct a game of Pipes from a file name.

        Parameters:
            game_file (str): name of the game file.
        """
        # #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        # self._board_layout = [[Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        # Tile('tile', True), Tile('tile', True)], [StartPipe(1), Tile('tile', True), Tile('tile', True), \
        # Tile('tile', True), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), Tile('tile', True), \
        # Tile('tile', True), Pipe('junction-t', 0, False), Tile('tile', True), Tile('tile', True)], [Tile('tile', True), \
        # Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('locked', False), Tile('tile', True)], \
        # [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), EndPipe(3), \
        # Tile('tile', True)], [Tile('tile', True), Tile('tile', True), Tile('tile', True), Tile('tile', True), \
        # Tile('tile', True), Tile('tile', True)]]
        #
        # self._playable_pipes = {'straight': 1, 'corner': 1, 'cross': 1, 'junction-t': 1, 'diagonals': 1, 'over-under': 1}
        # #########################COMMENT THIS SECTION OUT WHEN DOING load_file#######################
        self._playable_pipes, self._board_layout = self.load_file(game_file)
        self._starting_positions = None
        self._ending_positions = None
        self.end_pipe_positions()

    def get_board_layout(self):
        """
         Returns the board layout of the game

         Return(list<list<Tile, ...>>): a list of lists
        """
        return self._board_layout

    def get_playable_pipes(self):
        """
        get a dictionary of all the playable pipes (the pipe types) and number of times each pipe can be played.

        Return(dict<str:int>): a list of lists
        """
        return self._playable_pipes

    def change_playable_amount(self, pipe_name: str, number: int):
        """
         ​Add​the quantity of playable pipes of type specified by pipe_name to number (in the selection panel).

         Parameters:
            pipe_name(str): The name of the pipe
            number(int): The playable amount

        """
        self._playable_pipes[pipe_name] += number

    def get_pipe(self, position):
        """
        get the Pipe at the position or the tile if there is no pipe at that position.

        Parameters:
            position(tuple): The position of the pipe

        Return(Pipe/None): the Pipe or the tile at the position
        """
        row, col = position
        pipe_position = self._board_layout[row][col]
        if 0 <= row < len(self._board_layout) and 0 <= col < len(self._board_layout[0]): # ensure position is valid
            if pipe_position.get_id() == 'pipe' or pipe_position.get_id() == 'special_pipe':
                return pipe_position
            else:
                return Tile('tile', True)

    def set_pipe(self, pipe, position):
        """
        Place the specified pipe at the given position (row, col) in the game board. /
        The number of available pipes of the relevant type should also be updated.

        Parameters:
            pipe(Pipe(tuple)): Pile in game
            position(tuple): The position of the pipe
        """
        row, col = position
        if 0 <= row < len(self._board_layout) and 0 <= col < len(self._board_layout[0]):
            self._board_layout[row][col] = pipe
            self.change_playable_amount(pipe.get_name(), -1)

    def pipe_in_position(self, position):
        """
         Returns the pipe in the given position (row, col) of the game board if there is a Pipe in the given position./
          Returns None if the position given is None or if the object in the given position is not a Pipe

        Parameters:
            position(tuple): The position of the pipe

        Return(Pipe/None): return the Pipe or None
        """
        if position is not None and position[0] >= 0 and position[1] >= 0:
            pipe = self.get_pipe(position)
            if pipe.get_id() == 'pipe' or pipe.get_id() == 'special_pipe':
                return pipe

    def remove_pipe(self, position):
        """
         Removes the pipe at the given position from the board (Hint: create an empty tile at the given (row, col) /
          position and increase the playable number of the given pipe).

        Parameters:
            position(tuple): The position of the pipe
        """
        row, col = position
        if 0 <= row < len(self._board_layout) and 0 <= col < len(self._board_layout[0]):
            removed_pipe_name = self._board_layout[row][col].get_name()
            self.change_playable_amount(removed_pipe_name, 1)
            self._board_layout[row][col] = Tile(EMPTY_TILE, True)

    def position_in_direction(self, direction, position):
        """
        Find the pipe in the given position (row, col) of the game board

        Parameters:
            direction(int): The direction of the pipe
            position(tuple): The position of the pipe

        Returns(tuple<str, tuple<int, int>>): return the Pipe or None
        """
        row, col = position
        pipe_dir = DIRECTION.index(str(direction))
        new_direction = DIRECTION[(pipe_dir + 2) % 4]
        if 0 <= row < len(self._board_layout) and 0 <= col < len(self._board_layout[0]):
            change_step = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)} # the relationship between two pipes
            # the abscissa and ordinate of the new position
            new_col, new_row = row + change_step[str(direction)][0], col + change_step[str(direction)][1]
            if 0 <= new_row < len(self._board_layout) and 0 <= new_col < len(self._board_layout[0]):
                return new_direction, (new_col, new_row)

    def end_pipe_positions(self):
        """
        Find and save the start and end pipe positions from the game board
        """
        abscissa = 0
        ordinate = 0
        for row in self._board_layout:
            for t_pipe in row:
                if t_pipe.get_name() == 'start':
                    self._starting_positions = (abscissa, ordinate)
                elif t_pipe.get_name() == 'end':
                    self._ending_positions = (abscissa, ordinate)
                ordinate += 1
            ordinate = 0
            abscissa += 1

    def get_starting_position(self):
        """
        get the (row, col) position of the start pipe.

        Returns(tuple<int, int>): Start pipe position.

        """
        return self._starting_positions

    def get_ending_position(self):
        """
         Returns:
             self._ending_positions(tuple):the position of the endpipe
         """
        return self._ending_positions

    #########################UNCOMMENT THIS FUNCTION WHEN READY#######################
    def check_win(self):
        """
        (bool) Returns True  if the player has won the game False otherwise.
        """
        position = self.get_starting_position()
        pipe = self.pipe_in_position(position)
        queue = [(pipe, None, position)]
        discovered = [(pipe, None)]
        while queue:
            pipe, direction, position = queue.pop()
            for direction in pipe.get_connected(direction):

                if self.position_in_direction(direction, position) is None:
                    new_direction = None
                    new_position = None
                else:
                    new_direction, new_position = self.position_in_direction(direction, position)
                if new_position == self.get_ending_position() and direction == self.pipe_in_position(
                        new_position).get_connected()[0]:
                    return True

                pipe = self.pipe_in_position(new_position)
                if pipe is None or (pipe, new_direction) in discovered:
                    continue
                discovered.append((pipe, new_direction))
                queue.append((pipe, new_direction, new_position))
        return False

    #########################UNCOMMENT THIS FUNCTION WHEN READY#######################

    def load_file(self, filename):
        """
         Implement the following function to allow board_layout and playable_pipes to be set according to a .csv file /
         and integrate this functionality as a method in the PipeGame class

        Parameters:
            filename(str): The name of the file

        Returns(tuple<str, tuple<int, int>>):  Returns appropriate values for playable_pipes and board_layout
        """
        with open(filename, 'r') as file:
            game_list = []
            for line in file:
                line = line.strip()
                line_list = line.split(',')
                game_list.append(line_list)
            board_layout_list = game_list[: -1]
            playable_pipes_list = game_list[-1]

            playable_pipes = {}
            n = 0
            for pipe in PIPES.values(): # Constract the playable_pipes dictionary
                playable_pipes[pipe] = int(playable_pipes_list[n])
                n += 1
            board_layout = []  # The outside list of the board_layout
            for row_list in board_layout_list:
                inside_new_board = []  # The inside list of the board_layout
                for in_list in row_list:
                    if len(in_list) == 3:  # add the locked pipe into the map
                        orientation = in_list[-1]
                        type2 = in_list[:-1]
                        tile = Pipe(PIPES[type2], int(orientation), False)
                    elif len(in_list) == 2:  # add the start and end pipe into the board_layout
                        end_char = in_list[-1]
                        if end_char.isdigit():
                            type2 = in_list[0]
                            orientation = in_list[-1]
                            if type2 == 'S':
                                tile = StartPipe(int(orientation))
                            elif type2 == 'E':
                                tile = EndPipe(int(orientation))
                        else:
                            tile = Pipe(PIPES[in_list], 0, False)  # while the orientation of the locked pipe is 0
                            print(tile)
                    else:
                        if in_list == '#':
                            tile = Tile(EMPTY_TILE)
                        elif in_list == 'S':
                            tile = Tile(SPECIAL_TILES[in_list])
                        elif in_list == 'E':
                            tile = EndPipe(int(orientation))
                        elif in_list == 'L':
                            tile = Tile('locked', False)
                    inside_new_board.append(tile)
                board_layout.append(inside_new_board)
                self._playable_pipes = playable_pipes
                self._board_layout = board_layout
            return self._playable_pipes, self._board_layout


class Tile:
    """
    A class of Tiles.
    """
    def __init__(self, name, selectable=True):
        """
        initialize the Tile class

        Parameters:
            name(str): the name of the Tile class
            selectable(bool): the status of the Tile class
        """

        self._name = name
        self._selectable = selectable

    def get_name(self):
        """Get the name of the Tile

        Returns:
             self._name(str):the name of the Tile class
        """
        return self._name

    def get_id(self):
        """Get the id of the tile

        Returns:
            Tile_id(str):the id of the tile
        """
        return "tile"

    def set_select(self, select: bool):
        """Sets the status of the select switch to True ​or False​.

        Parameters:
            select(bool):the status of the select Tile
        """
        self._selectable = select

    def can_select(self):
        """Returns True if the tile is selectable, or False if the tile is not selectable.

        Returns:
            self._selectable(bool): the status of the Tile
        """
        return self._selectable

    def __str__(self):
        """Returns the string representation of the Tile

        Returns:
            (str):the representation of the tile
        """
        return f"{self.__class__.__name__}('{self._name}', {self._selectable})"

    __repr__ = __str__


class Pipe(Tile):
    """
    a class of Pipe

    """
    def __init__(self, name, orientation=0, selectable=True):
        """Construct the Pipe

        Parameters:
            name(str):the name of Pipe
            orientation(int):the orientation of the Pipe
            selectable(bool):the status of the Pipe
        """
        super().__init__(name, selectable)
        self._orientation = orientation

    def get_id(self):
        """"Returns the id of the Pipe class

        Returns:
            Pipe_id(str):the id of the Pipe class
        """
        return 'pipe'

    def get_connected(self, side):
        """Returns a list of all sides that are connected to the given side or empty list if invalid

        Parameters:
            side(str):the given side of the pipe

        Returns:
            (list):a list of all sides that are connected to the given side
        """
        pipe_dir = DIRECTION.index(side)  # the direction of the pipe
        if self.get_name() == PIPES['ST']:
            if pipe_dir == (self._orientation - 2) % 4 or pipe_dir == self._orientation:
                return []
            else:
                return [DIRECTION[(pipe_dir - 2) % 4]]

        elif self.get_name() == PIPES['CO']:

            if pipe_dir == self._orientation:
                return [DIRECTION[(pipe_dir + 3) % 4]]
            elif pipe_dir == (self._orientation + 3) % 4:
                return [DIRECTION[(pipe_dir + 1) % 4]]
            else:
                return []

        elif self.get_name() == PIPES['CR']:
            return [DIRECTION[(pipe_dir + 1) % 4], DIRECTION[(pipe_dir + 2) % 4], DIRECTION[(pipe_dir + 3) % 4]]

        elif self.get_name() == PIPES['JT']:
            if pipe_dir == self._orientation:
                return [DIRECTION[(pipe_dir + 1) % 4], DIRECTION[(pipe_dir + 2) % 4]]
            elif (pipe_dir == self._orientation + 1) % 4:
                return [DIRECTION[(pipe_dir + 1) % 4], DIRECTION[(pipe_dir + 3) % 4]]
            elif (pipe_dir == self._orientation + 2) % 4:
                return [DIRECTION[(pipe_dir + 2) % 4], DIRECTION[(pipe_dir + 3) % 4]]
            else:
                return []

        elif self.get_name() == PIPES['DI']:
            if pipe_dir == (self._orientation + 1) % 4 or pipe_dir == (self._orientation + 3) % 4:
                return [DIRECTION[(pipe_dir + 1) % 4]]
            elif pipe_dir == self._orientation or pipe_dir == (self._orientation + 2):
                return [DIRECTION[(pipe_dir + 3) % 4]]

        elif self.get_name() == PIPES['OU']:
            return [DIRECTION[(pipe_dir + 2) % 4]]

    def rotate(self, direction):
        """​Rotates the pipe one turn.A positive direction implies clockwise rotation,
        and a negative direction implies counter-clockwise rotation and 0 means no rotation.

        Parameters:
            direction(int):the direction you want turn

        Return:
            self._orientation(Pipe): The rotated pipe
        """
        self._orientation = (self._orientation + direction) % 4

    def get_orientation(self):
        """Returns the orientation of the pipe

        Returns:
            self._orientation(int):the orientation of the pipe
        """
        return self._orientation

    def __str__(self):
        """Returns the string representation of the Pipe

        Returns:
            (str):the representation of the pipe
        """
        return f"{self.__class__.__name__}('{self._name}', {self._orientation})"

    __repr__ = __str__


class SpecialPipe(Pipe):
    """
    a class of special pipe
    """
    def __init__(self, name, orientation=0):
        """Construct the SpecialPipe class

         Parameters:
            name(str):the name of SpecialPipe
            orientation(int):the orientation of the SpecialPipe
        """
        super().__init__(name, orientation)
        self._selectable = False
        self._orientation = orientation

    def get_id(self):
        """ Get the id of the special pipe

         Return:
            (str): the id of the pipe
        """
        return "special_pipe"

    def __str__(self):
        """Returns the string representation of the SpecialPipe

        Returns:
            (str):the representation of the SpecialPipe
        """
        return f"{self.__class__.__name__}({self._orientation})"

    __repr__ = __str__


class StartPipe(SpecialPipe):
    """
    a class of start pipe
    """
    def __init__(self, orientation=0):
        """Construct the StartPipe

        Parameters:
            orientation(int):the orientation of the StartPipe
        """
        super().__init__(str(orientation))
        self._selectable = False
        self._orientation = orientation

    def get_connected(self, side=None):
        """Return the direction that the start pipe is facing.

        Parameters:
            side(bool):the status of the StartPipe

        Returns:
            connected_list(list):the direction that the start pipe is facing
        """
        connected_list = [DIRECTION[(self.get_orientation() + 3) % 4]]
        return connected_list

    def get_name(self):
        """ Get the name of the special pipe

         Return:
            (str): the name of the pipe
        """
        return "start"

    def __str__(self):
        """Returns the string representation of the StartPipe

        Returns:
            (str):the representation of the StartPipe
        """
        return f"{self.__class__.__name__}({self.get_orientation()})"

    __repr__ = __str__


class EndPipe(SpecialPipe):
    """
    a class of end pipe
    """
    def __init__(self, orientation=0):
        """Construct the StartPipe

        Parameters:
            orientation(int):the orientation of the EndPipe
        """
        super().__init__(str(orientation))
        self._selectable = False
        self._orientation = orientation

    def get_connected(self, side=None):
        """Return the direction that the end pipe is facing.

        Parameters:
            side(bool):the status of the EndPipe

        Returns:
            connected_side_list(list):the direction that the end pipe is facing
        """
        connected_list = [DIRECTION[(self.get_orientation() + 1) % 4]]
        return connected_list

    def get_name(self):
        """ Get the name of the special pipe

         Return:
            (str): the name of the pipe
        """
        return "end"

    def __str__(self):
        """Returns the string representation of the EndPipe

         Returns:
             (str):the representation of the EndPipe
         """
        return f"{self.__class__.__name__}({self._orientation})"

    __repr__ = __str__


def main():
    """
    main function of the game
    """
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
