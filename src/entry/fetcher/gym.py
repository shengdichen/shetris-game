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

from src.engine.engine import Engine
from src.entry.fetcher.base import Corrector


class Unpacker:
    """
    Unpack gym's command

    1.  do not do any processing

    """

    @staticmethod
    def multi_2(action: np.ndarray) -> tuple[int, int]:
        """
        Unpack a gym's 2-tuple

        Usage:
        action-space is a 2-length MultiDiscrete: ([*, *])

        :param action:
        :return:
        """

        return action[0], action[1]

    @staticmethod
    def tuple_d_md(action):
        """
        Unpack

        Usage:
        action-space is a 2-tuple: Tuple(D, MultiD)

        :param action:
        :return:
        """

        return action[0], action[1]

    @staticmethod
    def tuple_md_md(action):
        """
        Usage:
        action-space is a 2-tuple: Tuple(MultiD, MultiD)

        :param action:
        :return:
        """

        return action[0], action[1]


class FetcherGym:
    """
    0.  Got an unpacked command from gym
    1.  do some pre-processing: make it ready for engine

    """

    @staticmethod
    def get_pre_corrected(engine: Engine, action: np.ndarray) -> tuple[bool, int, int]:
        """
        Correct the action to be within limit
        0.  manually unpack the action into a tuple
        1.  correct the action

        :param engine:
        :param action:
        :return:
        """

        pre_rot, pre_pos1 = action[0], action[1]

        valid_range_shifted = engine.mover.analyzer.get_shifted_range1(
            engine.pid, pre_rot
        )
        corrected, pre_pos1_corrected = Corrector.correct_to_max(
            pre_pos1, valid_range_shifted[1]
        )

        return corrected, pre_rot, pre_pos1_corrected

    @staticmethod
    def get_pre(action) -> tuple[int, int]:
        """
        Just a pass-through, no correction

        :param action:
        :return:
        """

        return action


if __name__ == "__main__":
    pass
