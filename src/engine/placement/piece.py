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

    def new_from_multi_pos(self, delta: np.ndarray):
        """
        Create new from change in (pos0, pos1).
        Used for trying out srs-shift candidates

        :param delta:
        :return:
        """

        return Config(self.pos + delta, self.rot)

    def new_from_multi_pos1_rot(self, delta_pos1: int, delta_rot: int) -> "Config":
        """
        Create new from change in (pos1, rot).
        Used for every:
        1.  bot-move
        2.  pre-move

        :param delta_pos1:
        :param delta_rot:
        :return:
        """

        return Config(self.pos + np.array((0, delta_pos1)), self.rot + delta_rot)

    def new_from_multi(self, delta: "Config"):
        """
        factory: create new after shifting from delta; the new pos is copied
        with np.copy(); thus no worries about safety

        :param delta: change by this config
        :return: a new config-object
        """

        pos_delta, rot_delta = Config.unpack(delta)

        return Config(
            self.pos + pos_delta,
            self.rot + rot_delta,
        )

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

    # typical srs-attempt
    c_tmp = c.new_from_multi_pos(np.array([10, -10]))
    print(c_tmp)

    # typical multi (by bot)
    c_delta = Config(np.array([0, 7]), -2)
    c_tmp = c.new_from_multi(c_delta)
    print(c_tmp)

    c.assign(c_tmp)
    print(c)


class Piece:
    """
    This stores everything about the current piece:
    1.  the pid (which piece);
    2.  the config (in which config is the piece);
    3.  the coord (the four coordinates of the piece in its config).

    The coord is fetched from CoordFactory with:
    1.  the pid
    2.  the config.

    """

    def __init__(
        self,
        pid: Optional[int] = None,
        config: Optional[Config] = None,
        coord: Optional[np.ndarray] = None,
    ):
        """
        It really makes no sense to provide default values from these: as any
        piece in any config is possible.
        Instead, we will rely on the classmethods below to construct objects.

        """

        self._pid = pid
        self._config = config
        self._coord = coord

    def __str__(self):
        """
        Print the coordinates in transposed form, makes for a more compact
        (less rows) output.

        """

        if self.coord is None:
            return "[Piece] id={0} | {1}\n{2}".format(self.pid, self.config, self.coord)
        return "[Piece] id={0} | {1}\n{2}".format(
            self.pid, self.config, self.coord.transpose()
        )

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, value: int):
        self._pid = value

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value: Config):
        self._config.assign(value)

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, value: np.ndarray):
        self._coord = value

    @classmethod
    def from_init(cls, pid: int, config: Config) -> "Piece":
        """
        Called when a piece is newly created: at this state, we only have:
        1.  its pid
        2.  its config
        ; this is seen as the "init"-step
        to calculate its coordinates from its config.

        :param pid: pid of piece
        :param config: config of piece
        :return:
        """

        coord = CoordFactory.get_coord(pid, config)
        return cls(pid, config, coord)

    @classmethod
    def from_atomic_pos0(cls, piece: "Piece", positive_dir: bool) -> "Piece":
        """
        Construct the new piece-info after an atomic-pos0.
        NOTE:
        The new coordinates are easily found by just shifting the existing
        coordinates.

        :param piece: current piece-info
        :param positive_dir:
        :return:
        """

        config_new = piece.config.new_from_atomic_pos0(positive_dir)

        delta = 1 if positive_dir else -1
        coord_new = piece.coord + np.array([delta, 0])

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_atomic_pos1(cls, piece: "Piece", positive_dir: bool) -> "Piece":
        """
        Construct the new piece-info after an atomic-pos1.
        NOTE:
        The new coordinates are easily found by just shifting the existing
        coordinates.

        :param piece: current piece-info
        :param positive_dir:
        :return:
        """

        config_new = piece.config.new_from_atomic_pos1(positive_dir)

        delta = 1 if positive_dir else -1
        coord_new = piece.coord + np.array([0, delta])

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_atomic_rot(cls, piece: "Piece", positive_dir: bool) -> "Piece":
        """
        Construct the new piece-info after an atomic-rot.
        NOTE:
        Since the rotation is modified, must fetch the new coordinates
        from CoordsFactory.

        :param piece: current piece-info
        :param positive_dir:
        :return:
        """

        config_new = piece.config.new_from_atomic_rot(positive_dir)
        coord_new = CoordFactory.get_coord(piece.pid, config_new)

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_multi_pos0(cls, piece: "Piece", delta: int) -> "Piece":
        """
        Multi-shift in pos0.
        You probably should not be calling this:
        1.  Either this is a type and should be multi_pos1
        2.  Or you should perform hard-drop instead

        :param piece:
        :param delta:
        :return:
        """

        config_new = piece.config.new_from_multi_pos0(delta)
        coord_new = piece.coord + np.array([delta, 0])

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_multi_pos1(cls, piece: "Piece", delta: int) -> "Piece":
        """
        Multi-shift in pos1

        :param piece:
        :param delta:
        :return:
        """
        config_new = piece.config.new_from_multi_pos1(delta)
        coord_new = piece.coord + np.array([0, delta])

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_multi_rot(cls, piece: "Piece", delta: int) -> "Piece":
        config_new = piece.config.new_from_multi_rot(delta)
        coord_new = CoordFactory.get_coord(piece.pid, config_new)

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_multi_pos(cls, piece: "Piece", delta: np.ndarray):
        """
        Used after an attempted srs-shift.

        :param piece: current piece
        :param delta: composite-move, i.e., delta of (pos0, pos1)
        :return:
        """

        config_new = piece.config.new_from_multi_pos(delta)
        coord_new = piece.coord + delta

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_multi_pos1_rot(
        cls, piece: "Piece", delta_pos1: int, delta_rot: int
    ) -> "Piece":
        """
        Used for
        1.  every bot-move
        2.  the pre-move

        :param piece:
        :param delta_pos1: Implicitly assumed to be not 0
        :param delta_rot: Implicitly assuemd to be not 0
        :return:
        """

        config_new = piece.config.new_from_multi_pos1_rot(delta_pos1, delta_rot)
        coord_new = CoordFactory.get_coord(piece.pid, config_new)

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def from_multi(cls, piece: "Piece", delta: Config) -> "Piece":
        """
        Used after a multi. Typically a bot-move.

        :param piece:
        :param delta:
        :return:
        """

        config_new = piece.config.new_from_multi(delta)
        coord_new = CoordFactory.get_coord(piece.pid, config_new)

        return cls(piece.pid, config_new, coord_new)

    @classmethod
    def to_absolute(cls, piece: "Piece", target: Config) -> "Piece":
        curr_config = piece.config
        diff_config = Config(target.pos - curr_config.pos, target.rot - curr_config.rot)

        return Piece.from_multi(piece, diff_config)

    @classmethod
    def to_absolute_pos(cls, piece: "Piece", target_pos: np.ndarray):
        """
        Used in the init-phase to fetch in the ZERO-position.

        :param piece:
        :param target_pos:
        :return:
        """
        curr_pos = piece.config.pos
        diff_pos = target_pos - curr_pos

        return Piece.from_multi_pos(piece, diff_pos)


def run_piece():
    piece = Piece()
    print(piece)

    # a new piece is spawned
    pid = 1
    # initial-move
    config = Config(np.array([0, 2]), 3)
    piece = Piece.from_init(pid, config)
    print(piece)

    # perform atomic-rot
    piece = Piece.from_atomic_rot(piece, True)
    print(piece)

    # assuming atomic-rot failed: try srs-shift
    piece = Piece.from_multi_pos(piece, np.array((1, 2)))
    print(piece)

    piece = Piece.to_absolute_pos(piece, np.array((1, 7)))
    print(piece)


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
