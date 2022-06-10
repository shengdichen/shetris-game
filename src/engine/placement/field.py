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


class Field:
    def __init__(self, field: np.ndarray):
        self._field = field
        self._size = field.shape

    @property
    def field(self):
        return self._field

    @property
    def size(self):
        return self._size

    def print_field(self):
        """
        print every entry as 1 or 0, instead of True or False,
        making for a nicely aligned field in terminal-output

        """

        def print_bool_as_int(my_bool):
            return str(int(my_bool))

        np.set_printoptions(formatter={"bool": print_bool_as_int})
        print(self.field)

        # reset printoptions
        np.set_printoptions()


if __name__ == "__main__":
    pass
