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


class IndexFactory:
    """
    np's advanced-indexing is great for its namesake: indexing; but is
    relatively awkward to manipulate per se. This, however, is much required
    since indexes are shifted whenever a non-rotational move is performed.

    This factory provides routines to simplify such manipulations.

    """

    @staticmethod
    def make_shifted_pos0(idx: tuple[np.ndarray, np.ndarray], shift: int):
        """
        Move provided indexes in pos0.
        Pass in a positive value to move all non-zero entries DOWNWARDS.

        Used for:
        1.  performing a pos0-move
        2.  line-clear (shifting lines downwards).

        :param idx: indexes to move
        :param shift: positive-values for shifting downwards, negative-values
        for shifting upwards
        :return:
        """

        return idx[0] + shift, idx[1]

    @staticmethod
    def make_shifted_pos1(idx: tuple[np.ndarray, np.ndarray], shift: int):
        """
        Move provided indexes in pos1.

        Used for:
        1.  performing a pos1-move.

        :param idx: indexes to move
        :param shift: positive-values for shifting right, negative-values for
        shifting left
        :return:
        """

        return idx[0], idx[1] + shift


if __name__ == "__main__":
    pass
