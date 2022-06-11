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
from src.engine.placement.field import Field
from src.engine.placement.mover import Mover
from src.engine.placement.piece import Piece


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

    @staticmethod
    def make_field(size: tuple[int, int]) -> Field:
        """
        Produce an all empty field of our desired size.

        :return: the Field object.
        """

        from src.util.fieldfac import FieldFactory

        return Field(FieldFactory.get_all_zeros(size))

    @staticmethod
    def _make_test_field() -> Field:
        """
        Produce the test field.

        :return: the Field object.
        """

        from src.util.fieldfac import FieldReader

        return Field(FieldReader.read_from_file())


if __name__ == "__main__":
    pass
