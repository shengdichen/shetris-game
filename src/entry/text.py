# The Tetris-Implementation of the Shetris-Project, written from scratch.
#
# Copyright (C) 2022 Shengdi 'shc' Chen (me@shengdichen.xyz)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


import numpy as np

from src.engine.generator.baggen import Generator
from src.engine.placement.field import Field
from src.engine.placement.mover import Mover
from src.engine.placement.piece import Config, Piece
from src.entry.fetcher import _InputConverter


class EntryText:
    """
    This provides the step() of the game:
    1.  Defines the game-framework:
        1.  game-over constant
        2.  the main-loop
    2.  Interaction with all placement-components:
        1.  generate pid
        2.  initial placement (put)
        3.  input-modes:
            1.  atomic (human)
            2.  multi (botterminal)
    3.  prompter for user-input:
        1.  atomic-mode: ask for atomics
        2.  multi-mode: ask for multi

    4.  perform the moves:
        1.  atomic
        2.  multi

    What this should NOT do:
    1.  Process the moves:
        ->  This should be handled by the engine
    1.  actually launch the game:
        ->  This should really be in main(); this entry just provides the game
            library

    """

    def __init__(self):
        self._field = self.make_field()
        self.field.print_field()
        self._size = self.field.size

        self._pid = 0
        self._generator = Generator()

        self._piece = None
        self._mover = Mover(self.field)
        self._is_game_over = False

    @property
    def field(self):
        return self._field

    @field.setter
    def field(self, value):
        self._field = value

    @property
    def size(self):
        return self._size

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value):
        self._pid = value

    @property
    def generator(self):
        return self._generator

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, value):
        self._piece = value

    @property
    def mover(self):
        return self._mover

    @property
    def is_game_over(self):
        return self._is_game_over

    @is_game_over.setter
    def is_game_over(self, value):
        self._is_game_over = value

    @staticmethod
    def make_field() -> Field:
        """
        Produce an all empty field of our desired size.

        :return: the Field object.
        """

        from src.util.fieldfac import FieldFactory
        return Field(FieldFactory.get_all_zeros((20, 10)))

        # from src.fetcher.fieldfac import FieldReader
        # return Field(FieldReader.read_from_file())

    def main_loop(self):
        """
        The main loop of the game:
        1. generate the new piece:
        2. check if game is over:
            a. NO: perform the main loop
            b. YES: clean-up

        :return: None
        """

        while True:
            self.init()

            if not self.is_game_over:
                self.piece_loop()
                self.piece_finish()
            else:
                self.clean_up()
                break

        # the non-while-true implementation
        while not self.is_game_over:
            self.init()
            if not self.is_game_over:
                self.piece_loop()
                self.piece_finish()
        self.clean_up()

    def init(self):
        """
        The init-step:
        1.  Generates a piece
        2.  Prompt for pre-move, perform it if existent
        3.  Check if game-over based on the pre-moved piece-info

        :return:
        """

        self.gen_piece()
        self.pre_move()
        self.check_game_over()

    def gen_piece(self):
        """
        1.  Generate new pid;
        2.  Set the default (-4, 0, 0) config
        3.  Generate the corresponding piece-information.

        """

        self.pid = self.generator.get_pids()

        config = Config(np.array([-4, +0]), +0)
        self.piece = Piece.from_init(self.pid, config)
        print("Piece inited:", self.piece)

    def pre_move(self):
        """
        Perform the pre-move by modifying self.piece.
        This is NOT called with Mover, as we are disregarding the field at this point;
        Also, calling Mover will of course fail, because our height is at -4.
        NOTE:
        We must handle the 0-case, as Mover always expects != 0 delta for moving.

        :return:
        """

        delta_pos1, delta_rot = _InputConverter.prompt_pre_raw()
        if not delta_rot == 0:
            self.piece = Piece.from_multi_rot(self.piece, delta_rot)
        if not delta_pos1 == 0:
            self.piece = Piece.from_multi_pos1(self.piece, delta_pos1)

    def check_game_over(self):
        """
        Check if game-over by applying the pre-move operation defined in the Mover.
        Set self.is_game_over to True if that fails, no-op otherwise.

        :return:
        """

        result = self.mover.attempt_pre(self.piece)
        if result is not None:
            self.piece = result
            print("Pre-Move SUCCESSFUL:", self.piece)
        else:
            print("Pre-Move FAILED, GAMEOVER")
            self.is_game_over = True

    def piece_loop(self):
        """
        Describes user
        1.  Prompt user's input, execute the input's corresponding move;
        2.  When input is empty (prompt_multi returns None):
            ->  Returns because user decides to stop moving

        NOTE:
        User is guaranteed to be able to provide an input, it is then up to the user
        to decide if the first chance of providing input is already the last, i.e.,
        do not move the piece at all (just hit Enter, i.e., do not enter anything).

        :return:
        """

        # do-while style: guarantee (at least) the first prompt
        multi = _InputConverter.prompt_multi()

        while multi is not None:
            move_type, delta = multi
            self.move_piece(move_type, delta)
            multi = EntryText.prompt_multi()
        print("This piece is done!")

    def move_piece(self, move_type: int, delta: int) -> None:
        """
        Handle a move: a thin wrapper of the mover:
        1.  atomic
        2.  or multi

        :param move_type: 0 for pos0, 1 for pos1; everything else for rot
        :param delta: how much to move (positive values in positive direction; negative ones
        in negative direction)
        :return:
        """

        piece_new = self.mover.attempt_multi(move_type, self.piece, delta)

        if piece_new is not None:
            self.piece = piece_new
            print(self.piece)
            print("Move of: {0} @ {1} successful".format(move_type, delta))
        else:
            print("Move of: {0} @ {1} FAILED!".format(move_type, delta))

    def piece_finish(self):
        """
        0.  perform a hard-drop
        1.  Write the coordinates of the current piece to the field
        2.  Check if we have line clear

        NOTE:
        The last two operations are abstracted into the freeze()-function

        NOTE:
        This can be thought of as the step() function, i.e., the evolution mechanism
        of a control-problem.

        :return:
        """

        self.piece = self.mover.attempt_drop(self.piece)
        self.mover.freeze(self.piece)
        self.field.print_field()

    def clean_up(self):
        """
        1.  Perform clean-ups;
        2.  Quit the game.

        :return:

        """

        self.field.print_field()
        print("Quitting game.")


def gameraw_test():
    g = EntryText()
    g.main_loop()


if __name__ == "__main__":
    gameraw_test()
