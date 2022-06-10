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


from typing import Optional

import numpy as np

from src.engine.placement.field import Field
from src.engine.placement.piece import Piece


class Mover:
    """
    Tell me a move:
    1.  atomic
    2.  multi
    and I will give you:
    1.  if successful: the new piece-info
    2.  if not: None, as a signal of failure

    """

    check_string_to_check_tuple = {
        "U": [True, False],
        "D": [True, True],
        "L": [False, False],
        "R": [False, True],
    }

    def __init__(self, field: Field) -> None:
        """
        Tell the Mover to use some field.

        :param field: the field to use
        """

        self._field = field

    @property
    def field(self):
        return self._field

    @staticmethod
    def _atomic_to_check_string(atomic_type: int, positive_dir: bool) -> str:
        """
        Get the boundary-check-string of an atomic:
        i.  if moving left: check left-boundary;
        ii. if moving right: check right-boundary;
        etc.
        Otherwise, check all boundaries

        :param atomic_type: 0 for pos0; 1 for pos1; anything else for rot
        :param positive_dir: True if the atomic is in negative sense; False
        otherwise
        :return:
        """

        if atomic_type == 0:
            if positive_dir:
                check_string = "D"
            else:
                check_string = "U"
        elif atomic_type == 1:
            if positive_dir:
                check_string = "R"
            else:
                check_string = "L"
        else:
            check_string = "LRUD"

        return check_string

    def _failed_boundaries_collision(
        self, check_string: str, candidates: np.ndarray
    ) -> bool:
        """
        Check if boundaries- or collision-checks failed.

        NOTE:
        This is our standard check for any move: both atomic and multi.

        NOTE:
        Short-circuiting is used: boundary-checks are performed first, then the
        collision check. Returns As soon as one check fails. This ordering is
        intentional: the field is expected to be generally unoccupied, thus,
        the chances of exceeding some boundary (or boundaries) are expected to
        be higher than that of producing a collision.

        :param check_string: which boundaries to check
        :param candidates: potential coordinates (usually 4 of a piece)
        :return: True if failed checks (bad candidates); False otherwise
        """

        if self.field.exceeded_boundaries(check_string, candidates):
            return True

        if self.field.has_collision(candidates):
            return True

        return False

    def _attempt_atomic_pos(
        self, piece: Piece, in_pos0: bool, positive_dir: bool
    ) -> Optional[Piece]:
        """
        Attempt an atomic in pos0 or pos1.
        1.  first convert an atomic to the cooresponding check-string
        2.  perform the boundary-collision check

        :param piece: initial piece-information
        :param in_pos0: True if atomic in pos0; False otherwise (pos1)
        :param positive_dir: True if moving in positive direction; False else
        :return: None if the move failed; the new coords if succeeded
        """

        if in_pos0:
            check_string = Mover._atomic_to_check_string(0, positive_dir)
            piece_new = Piece.from_atomic_pos0(piece, positive_dir)
        else:
            check_string = Mover._atomic_to_check_string(1, positive_dir)
            piece_new = Piece.from_atomic_pos1(piece, positive_dir)

        if self._failed_boundaries_collision(check_string, piece_new.coord):
            return None
        return piece_new


if __name__ == "__main__":
    pass
