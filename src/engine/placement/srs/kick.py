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


class Kick:
    """
    The data of SRS for "kick"-actions after a failed rotation, specifically,
    when a rotation failed initially from direct read of SRS's coordinates
    data, the state after this failed rotation is then subjected to various
    attempts of positional shifts, metaphorically kicking this state into a
    shifted state that does not fail, i.e., within all boundaries and does not
    collide with the field.

    In particular, this enables the more "modern" movements such as:
    1.  kicks
        a.  wall-kick
            https://tetris.wiki/Wall_kick
        b.  floor-kick
            https://tetris.wiki/Floor_kick
    2.  spins
        a.  T-spins
        b.  S/Z-spins
        c.  L/J-spins
        d.  I-spins
            https://tetris.wiki/I-Spins_in_SRS

    R(3) -> 0(0)  (pos-rot)
    L(1) -> 0(0)  (neg-rot)

    0(0) -> L(1) 	(pos-rot)
    2(2) -> L(1) 	(neg-rot)

    L(1) -> 2(2) 	(pos-rot)
    R(3) -> 2(2) 	(neg-rot)

    2(2) -> R(3) 	(pos-rot)
    0(0) -> R(3) 	(neg-rot)

    """

    srs_o = np.array((((+0, +0),),))

    srs_i = np.array(
        (
            ((+0, +0), (+0, +2), (+0, -1), (-1, +2), (+2, -1)),
            ((+0, +0), (+0, +1), (+0, -2), (+2, +1), (-1, -2)),
            ((+0, +0), (+0, -1), (+0, +2), (-2, -1), (+1, +2)),
            ((+0, +0), (+0, +2), (+0, -1), (-1, +2), (+2, -1)),
            ((+0, +0), (+0, -2), (+0, +1), (+1, -2), (-2, +1)),
            ((+0, +0), (+0, -1), (+0, +2), (-2, -1), (+1, +2)),
            ((+0, +0), (+0, +1), (+0, -2), (+2, +1), (-1, -2)),
            ((+0, +0), (+0, -2), (+0, +1), (+1, -2), (-2, +1)),
        )
    )

    srs_szljt = np.array(
        (
            ((+0, +0), (+0, +1), (+1, +1), (-2, +0), (-2, +1)),
            ((+0, +0), (+0, -1), (+1, -1), (-2, +0), (-2, -1)),
            ((+0, +0), (+0, +1), (-1, +1), (+2, +0), (+2, +1)),
            ((+0, +0), (+0, +1), (-1, +1), (+2, +0), (+2, +1)),
            ((+0, +0), (+0, -1), (+1, -1), (-2, +0), (-2, -1)),
            ((+0, +0), (+0, +1), (+1, +1), (-2, +0), (-2, +1)),
            ((+0, +0), (+0, -1), (-1, -1), (+2, +0), (+2, -1)),
            ((+0, +0), (+0, -1), (-1, -1), (+2, +0), (+2, -1)),
        )
    )

    @staticmethod
    def get_srs_candidates(pid: int, rot: int, positive_dir=True) -> np.array:
        """
        Fetch all srs-shift candidates of the current configuration.

        NOTE:
        The SRS-mechanism is called if and only if a move-rotation fails.

        :param pid: which piece
        :param rot: config-rot (before move-rotation!)
        :param positive_dir: True if CCW-rotation (positive), else FALSE
        :return: potential shifts-of-center to try ending the rotation at
        """

        print(
            "SRS-triggered.\npid: {0}; rot: {1}, dir: {2}".format(
                pid, rot, positive_dir
            )
        )
        if pid == 0:
            srs_shifts_candidates = Kick.srs_i
        else:
            idx = 2 * rot + (1 - positive_dir)
            if pid == 1:
                srs_shifts_candidates = Kick.srs_i[idx]
            else:
                srs_shifts_candidates = Kick.srs_szljt[idx]
            print("Accessing SRS index: {0}".format(idx))

        print("SRS candidates are:{0}".format(srs_shifts_candidates))
        return srs_shifts_candidates


if __name__ == "__main__":
    pass
