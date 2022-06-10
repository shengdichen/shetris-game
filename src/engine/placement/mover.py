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

from src.engine.placement.field import Field


class Mover:
    """
    Tell me a move:
    1.  atomic
    2.  multi
    and I will give you:
    1.  if successful: the new piece-info
    2.  if not: None, as a signal of failure

    """

    def __init__(self, field: Field) -> None:
        """
        Tell the Mover to use some field.

        :param field: the field to use
        """

        self._field = field

    @property
    def field(self):
        return self._field

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


if __name__ == "__main__":
    pass
