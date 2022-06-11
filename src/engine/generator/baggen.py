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


class _Reservoir:
    def __init__(self, refill_threshold: int):
        self._data = np.empty(0, dtype=np.uint8)
        self._refill_threshold = refill_threshold

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def refill_threshold(self):
        return self._refill_threshold

    def refill(self, new_data: np.ndarray) -> None:
        """
        Refill the reservoir by the input.

        :param new_data:
        :return:
        """

        self.data = np.append(self.data, new_data)

    def need_refill(self) -> bool:
        """
        Check if a refill is necessary

        :return:
        """

        if self.data.size < self.refill_threshold:
            return True
        else:
            return False

    def read_pop_check(self, n_items: int) -> tuple[np.ndarray, bool]:
        """
        Does exactly the name-sake:
        1.  returns the first |n_items| items of the reservoir;
        2.  pop the very first item (by definition also the first item
        returned);
        3.  runs check to signal if a refill is necessary.

        Returns a tuple of (items, need_refill)
        :param n_items:
        :return:
        """

        items = self.data[0:n_items]
        self.data = self.data[1:]
        return items, self.need_refill()


if __name__ == "__main__":
    pass
