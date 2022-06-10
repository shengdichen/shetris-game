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


class FieldFactory:
    """
    Create the underlying (numpy) matrices of a field.

    """

    @staticmethod
    def get_all_zeros(size: tuple[int, int]) -> np.ndarray:
        """
        Produce a field of all zeros.

        :return: absolute path of this script
        """

        return np.zeros(size, dtype=bool)

    @staticmethod
    def get_all_ones(size: tuple[int, int]) -> np.ndarray:
        """
        Produce a field of all ones.

        :return: absolute path of this script
        """

        return np.ones(size, dtype=bool)


if __name__ == "__main__":
    pass
