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

from src.engine.placement.srs.coord import RelCoord


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

    def new_from_atomic_pos0(self, pos_dir: bool) -> "Config":
        """
        Create new from atomic-pos0.

        :param pos_dir: True if in positive direction, False otherwise
        :return:
        """

        delta = 1 if pos_dir else -1
        return Config(self.pos + np.array([delta, 0]), self.rot)

    def new_from_atomic_pos1(self, pos_dir: bool) -> "Config":
        """
        Create new from atomic-pos1.

        :param pos_dir: True if in positive direction, False otherwise
        :return:
        """

        delta = 1 if pos_dir else -1
        return Config(self.pos + np.array([0, delta]), self.rot)

    def new_from_atomic_rot(self, pos_dir: bool) -> "Config":
        """
        Create new from atomic-rot.

        :param pos_dir: True if in positive direction, False otherwise
        :return:
        """

        delta = 1 if pos_dir else -1
        return Config(self.pos, (self.rot + delta) % 4)

    def new_from_multi_pos0(self, delta: int) -> "Config":
        """
        Create new from multi-pos0.

        :param delta: how much to move in pos0.
        :return:
        """

        return Config(self.pos + np.array([delta, 0]), self.rot)

    def new_from_multi_pos1(self, delta: int) -> "Config":
        """
        Create new from multi-pos1.

        :param delta: how much to move in pos1.
        :return:
        """

        return Config(self.pos + np.array([0, delta]), self.rot)

    def new_from_multi_rot(self, delta: int) -> "Config":
        """
        Create new from multi-rot.

        :param delta: how much to move in rot.
        :return:
        """

        return Config(self.pos, self.rot + delta)

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


def run_config():
    c = Config(np.array([1, 1]), 4)
    print(c)

    # typical atomic
    c_tmp = c.new_from_atomic_rot(False)
    print(c_tmp)

    c.assign(c_tmp)
    print(c)


class CoordFactory:
    """
    A state-less factory to construct the four coordinates of a piece.

    """

    @staticmethod
    def get_coord(pid: int, config: Config) -> np.ndarray:
        """
        Calculate the coords of some piece (pid) in some config.

        :param pid: which piece
        :param config: which config
        :return: coordinates of the piece in the config (4 * 2)
        """

        shifts = RelCoord.get_rel_coord(pid, config.rot)

        return config.pos + shifts

    @staticmethod
    def get_range(pid: int, config: Config, is_pos0: bool) -> np.ndarray:
        """
        The range of the piece relative to the 2D-position in the config.

        In particular, this is used to:
        1.  in pos0:
            ->  obtain the vertical range of a piece to perform the line-clear
            operation on
        2.  in pos1
            ->  obtain the initial ZERO-position of a piece in PRE-phase

        :param pid:
        :param config:
        :param is_pos0:
        :return:
        """

        rel_range = RelCoord.get_rel_range(pid, config.rot, is_pos0)
        # print("rel range:", rel_range)

        idx = 0 if is_pos0 else 1
        return config.pos[idx] + rel_range


def run_factory():
    pid = 1
    config = Config(np.array([5, 4]), 1)

    print(CoordFactory.get_coord(pid, config))


if __name__ == "__main__":
    pass
