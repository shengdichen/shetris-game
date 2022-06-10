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


class Config:
    """
    The part of a piece user-influence:
    1.  The ref-pos
    2.  The rot

    """

    def __init__(self, pos: np.ndarray = np.array([0, 0]), rot: int = 0):
        self._pos = np.copy(pos)
        self._rot = rot % 4

    def __str__(self):
        return "[Config] pos={0}; rot={1}".format(self.pos, self.rot)

    @staticmethod
    def unpack(obj: "Config") -> tuple[np.ndarray, int]:
        return obj.pos, obj.rot

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value: np.ndarray):
        # no need to use deepcopy!
        self._pos = np.copy(value)

    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, value: int):
        self._rot = value

    def assign(self, config_new: "Config") -> None:
        """
        Modify self to take over another config.

        :param config_new:
        :return:
        """

        self.pos, self.rot = Config.unpack(config_new)

    @classmethod
    def new_from_pos0(cls, pos0: int):
        return cls(np.array([pos0, 0]), 0)

    @classmethod
    def new_from_pos1(cls, pos1: int):
        return cls(np.array([0, pos1]), 0)

    @classmethod
    def new_from_rot(cls, rot: int):
        return cls(np.array([0, 0]), rot)


if __name__ == "__main__":
    pass
