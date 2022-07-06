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


class FrontText:
    def __init__(self, size: tuple[int, int]):
        self._size = size
        self._front = self.init_front()

    @property
    def front(self):
        return self._front

    @front.setter
    def front(self, value):
        self._front = value

    @property
    def size(self):
        return self._size

    def show(self):
        """
        print every entry as 1 or 0, instead of True or False,
        making for a nicely aligned field in terminal-output

        """

        def print_bool_as_int(my_bool):
            return str(int(my_bool))

        np.set_printoptions(formatter={"bool": print_bool_as_int})
        print("-------START-------")
        print(self.front)
        print("--------END--------\n\n")

        # reset printoptions
        np.set_printoptions()

    def init_front(self):
        return np.zeros(self.size, dtype=bool)

    def set_from_field(self, field: np.ndarray):
        self.front = field
        self.show()

    def set_from_coords(self, coords: np.ndarray, new_val: bool = True):
        for coord_0, coord_1 in coords:
            self.front[coord_0, coord_1] = new_val

        self.show()

    def _set_from_idx(self, idx: tuple[np.ndarray, np.ndarray], new_val: bool):
        self.front[idx] = new_val

    def set_from_pair(self, idx_old: tuple[np.ndarray, np.ndarray], idx_new: tuple[np.ndarray, np.ndarray]):
        self._set_from_idx(idx_old, False)
        self._set_from_idx(idx_new, True)

        self.show()

    def shift_test(self):
        idx_old = self.front.nonzero()
        idx_new = idx_old[0] - 1, idx_old[1]
        self.set_from_pair(idx_old, idx_new)
        # print(self.front[(idx_old[0] - 1, idx_old[1])])


if __name__ == "__main__":
    ft = FrontText((20, 10))
    ft.show()

    from src.util.fieldfac import FieldReader

    ft.set_from_field(FieldReader.read_from_file())

    init = np.array([[1, 0], [2, 0], [3, 0]])
    ft.set_from_coords(init)

    # new = np.array([[2, 3], [2, 4], [2, 5]])
    # ft.set_from_pair(init, new)

    ft.shift_test()
