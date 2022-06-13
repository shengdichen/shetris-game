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

from src.engine.generator.baggen import Sequencer
from src.engine.generator.base import Generator
from src.engine.placement.field import Field
from src.engine.placement.mover import Mover
from src.engine.placement.piece import Piece, CoordFactory, Config
from src.util.fieldfac import FieldFactory


class Engine:
    """
    This provides the logic of the game:
    1.  Defines the game-framework:
        1.  game-over constant
        2.  the main-loop
    2.  Interaction with all placement-components:
        1.  generate pid
        2.  initial placement (put)
        3.  input-modes:
            1.  atomic (human)
            2.  multi (bot)
    3.  Define all supported operations:
        1.  atomic moves
        2.  multi-moves
        3.  freeze
    4.  Perform all moves

    What this should NOT do:
    1.  Prompt for user's input:
        ->  This should be in an entry-application

    1.  actually launch the game:
        ->  This should really be in main(); this entry just provides the game
            library

    """

    def __init__(self, size: tuple[int, int]):
        self._field = self.make_field(size)
        self.field.print_field()
        self._size = self.field.size

        self._pid = None
        self._generator = Sequencer(np.arange(7))

        self._piece = None
        self._mover = Mover(self.field)
        self._is_game_over = False

    @property
    def field(self):
        return self._field

    @property
    def size(self):
        return self._size

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value: int):
        self._pid = value

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, value: Generator):
        self._generator = value

    @property
    def piece(self):
        return self._piece

    @piece.setter
    def piece(self, value: Piece):
        self._piece = value

    @property
    def mover(self):
        return self._mover

    @property
    def is_game_over(self):
        return self._is_game_over

    @is_game_over.setter
    def is_game_over(self, value: bool):
        self._is_game_over = value

    def reset(self) -> None:
        """
        A collection of default-resetting:
        1.  make the field all-zero
        2.  reset the Sequence generator
        3.  set to not game-over

        :return:
        """

        self.field.field = FieldFactory.get_all_zeros(self.size)
        self.generator = Sequencer(np.arange(7))
        self.is_game_over = False

    @staticmethod
    def make_field(size: tuple[int, int]) -> Field:
        """
        Produce an all empty field of our desired size.

        :return: the Field object.
        """

        return Field(FieldFactory.get_all_zeros(size))

    @staticmethod
    def _make_test_field() -> Field:
        """
        Produce the test field.

        :return: the Field object.
        """

        from src.util.fieldfac import FieldReader

        return Field(FieldReader.read_from_file())

    def init_piece(self) -> None:
        """
        The init-part of the PRE-phase:
        1.  generate a new pid
        2.  set to the (default) initial-config (-4, 0, 0);
            ->  boundary-checks: only out of the "Up"-boundary (by definition
            of the config- and SRS-model, always within the "Left" and "Right"
            boundary; and trivially within the "Down"-boundary)
            ->  collision-checks: no collision apparently, since out of field
        3.  Generate the corresponding piece-info

        """

        self.pid = self.generator.get_pids()[0]

        config = Config(np.array([-4, +0]), +0)
        self.piece = Piece.from_init(self.pid, config)
        print("Piece inited:", self.piece)

    def exec_pre(self, delta_rot: int, delta_pos1: int) -> None:
        """
        Handle the PRE-phase after init_piece() has been called, which
        guarantees the new pid and the piece-info based on the init-config of
        (-4, 0, 0)

        :return:
        """

        result_pre = self.mover.attempt_pre(self.piece, delta_rot, delta_pos1)

        if result_pre is not None:
            self.piece = result_pre
            print("PRE-Phase SUCCESSFUL:", self.piece)
        else:
            self.is_game_over = True
            print("PRE-Phase FAILED, GAMEOVER!")

    def exec_atomic(self, move_type: int, pos_dir: bool) -> None:
        """
        Handle an atomic (explicitly not a multi).

        Side-effects:
        1.  if move successful: self.piece is modified;
        2.  if move failed: self.piece is not modified.

        :param move_type: 0 for pos0, 1 for pos1; everything else for rot
        :type pos_dir: True if in positive-dir, False otherwise
        in negative direction)
        :return:
        """

        piece_new = self.mover.attempt_atomic(move_type, self.piece, pos_dir)

        if piece_new is not None:
            self.piece = piece_new
            print(self.piece)
            print("ATOMIC of: {0} @ {1} successful".format(move_type, pos_dir))
        else:
            print("ATOMIC of: {0} @ {1} FAILED!".format(move_type, pos_dir))

    def exec_multi(self, move_type: int, delta: int) -> None:
        """
        Handle a move: a thin wrapper of the mover:
        1.  atomic.
        2.  or multi.
        Side-effects:
        1.  if move successful: self.piece is modified;
        2.  if move failed: self.piece is not modified.

        :param move_type: 0 for pos0, 1 for pos1; everything else for rot
        :param delta: how much to move (positive values in positive direction;
        negative ones in negative direction)
        :return:
        """

        piece_new = self.mover.attempt_multi(move_type, self.piece, delta)

        if piece_new is not None:
            self.piece = piece_new
            print(self.piece)
            print("MULTI of: {0} @ {1} successful".format(move_type, delta))
        else:
            print("MULTI of: {0} @ {1} FAILED!".format(move_type, delta))

    def exec_maxout(self, move_type: int, pos_dir: bool) -> None:
        """
        Execute a maxout

        Note:
        One special case of this is the "drop", defined below.

        :param move_type: 0 for pos0, 1 for pos1; anything else for rot
        :param pos_dir: True for move in positive-direction, False otherwise
        :return:
        """

        self.piece = self.mover.attempt_maxout(move_type, self.piece, pos_dir)

    def exec_drop(self) -> None:
        """
        Execute the hard-drop

        :return:
        """
        self.piece = self.mover.attempt_drop(self.piece)

    def exec_freeze(self) -> None:
        """
        1.  write the final coordinates of the current piece to the field
        2.  obtain the vertical range of the piece
        3.  trigger the line-clear operation with this vertical range

        NOTE:
        A hard-drop is intentionally not included here:
        1.  it is up to an entry-application to make sure that a hard-drop has
        been performed before freezing a piece
        2.  the behavior of not hard-dropping might be desired

        :return:
        """

        self.field.set_many(self.piece.coord, True)

        vertical_range = CoordFactory.get_range(self.pid, self.piece.config, True)
        self.field.lineclear(vertical_range)

        self.field.print_field()

    def clean_up(self) -> None:
        """
        1.  perform any necessary clean-ups (non implemented here)
        2.  quit the game

        :return:

        """

        self.field.print_field()
        print("Quitting Shetris.")


if __name__ == "__main__":
    pass
