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


class RelCoord:
    """
    Give me the:

    1.  pid
    2.  pos
    3.  rot
    And I'll give you
    1.  its four relative-coordinates (relative to the ref-pos)
    2.  as a direct by-product, its vertical and horizontal range relative to
    the ref-pos

    Note on storage-order:
    1.  all data first sorted according to pid:
            O
            I
            S
            Z
            L
            J
            T
    2.  then sorted (for the same piece) according to its rotational-sense
            0
            1 (L, 1 counter-clockwise rotation from 0)
            2 (2, 2 counter-clockwise rotation from 0)
            3 (R, 3 counter-clockwise rotation from 0)
    """

    _rel_coords = np.array(
        (
            # O
            (
                ((+0, +1), (+1, +1), (+0, +2), (+1, +2)),
                ((+0, +1), (+1, +1), (+0, +2), (+1, +2)),
                ((+0, +1), (+1, +1), (+0, +2), (+1, +2)),
                ((+0, +1), (+1, +1), (+0, +2), (+1, +2)),
            ),
            # I
            (
                ((+1, +0), (+1, +1), (+1, +2), (+1, +3)),
                ((+0, +1), (+1, +1), (+2, +1), (+3, +1)),
                ((+2, +0), (+2, +1), (+2, +2), (+2, +3)),
                ((+0, +2), (+1, +2), (+2, +2), (+3, +2)),
            ),
            # S
            (
                ((+1, +0), (+0, +1), (+1, +1), (+0, +2)),
                ((+0, +0), (+1, +0), (+1, +1), (+2, +1)),
                ((+2, +0), (+1, +1), (+2, +1), (+1, +2)),
                ((+0, +1), (+1, +1), (+1, +2), (+2, +2)),
            ),
            # Z
            (
                ((+0, +0), (+0, +1), (+1, +1), (+1, +2)),
                ((+1, +0), (+2, +0), (+0, +1), (+1, +1)),
                ((+1, +0), (+1, +1), (+2, +1), (+2, +2)),
                ((+1, +1), (+2, +1), (+0, +2), (+1, +2)),
            ),
            # L
            (
                ((+1, +0), (+1, +1), (+0, +2), (+1, +2)),
                ((+0, +0), (+0, +1), (+1, +1), (+2, +1)),
                ((+1, +0), (+2, +0), (+1, +1), (+1, +2)),
                ((+0, +1), (+1, +1), (+2, +1), (+2, +2)),
            ),
            # J
            (
                ((+0, +0), (+1, +0), (+1, +1), (+1, +2)),
                ((+2, +0), (+0, +1), (+1, +1), (+2, +1)),
                ((+1, +0), (+1, +1), (+1, +2), (+2, +2)),
                ((+0, +1), (+1, +1), (+2, +1), (+0, +2)),
            ),
            # T
            (
                ((+1, +0), (+0, +1), (+1, +1), (+1, +2)),
                ((+1, +0), (+0, +1), (+1, +1), (+2, +1)),
                ((+1, +0), (+1, +1), (+2, +1), (+1, +2)),
                ((+0, +1), (+1, +1), (+2, +1), (+1, +2)),
            ),
        )
    )

    rel_range_o = np.array(
        (
            # ((lowest_pos0, high_pos0 + 1), (low_pos1, high_pos1 + 1))
            ((+0, +2), (+1, +3)),
            ((+0, +2), (+1, +3)),
            ((+0, +2), (+1, +3)),
            ((+0, +2), (+1, +3)),
        )
    )

    rel_range_i = np.array(
        (
            ((+1, +2), (+0, +4)),
            ((+0, +4), (+1, +2)),
            ((+2, +3), (+0, +4)),
            ((+0, +4), (+2, +3)),
        )
    )

    rel_range_szljt = np.array(
        (
            ((+0, +2), (+0, +3)),
            ((+0, +3), (+0, +2)),
            ((+1, +3), (+0, +3)),
            ((+0, +3), (+1, +3)),
        )
    )

    @staticmethod
    def get_rel_coord(pid: int, rot: int) -> np.ndarray:
        """
        Provide the four shifts of a:

        1.  pid (which piece)
        2.  rot (at which rotation)

        :param pid:
        :param rot:
        :return:
        """

        return RelCoord._rel_coords[pid][rot]

    @staticmethod
    def get_rel_range(pid: int, rot: int, is_pos0: bool) -> np.ndarray:
        """
        The range of the piece relative to the 2D-position in the config.

        In particular, this is used to:
        1.  obtain the ZERO-position (especially in pos1) of a piece in
        PRE-phase
        2.  obtain the vertical range of a piece to perform the line-clear
        operation on

        :param pid:
        :param rot:
        :param is_pos0:
        :return:
        """

        if pid == 0:
            rel_range_all = RelCoord.rel_range_o
        elif pid == 1:
            rel_range_all = RelCoord.rel_range_i
        else:
            rel_range_all = RelCoord.rel_range_szljt

        idx = 0 if is_pos0 else 1
        return rel_range_all[rot][idx]


def range_test():
    from src.engine.placement.piece import Config, Piece, CoordFactory

    pid = 6
    config = Config(np.array([15, 10]), 1)
    piece = Piece.from_init(pid, config)

    print(piece)
    print("range0:", CoordFactory.get_range(pid, config, True))
    print("range1:", CoordFactory.get_range(pid, config, False))


if __name__ == "__main__":
    range_test()
