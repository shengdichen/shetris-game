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


from abc import ABC

import numpy as np

from src.engine.engine import Engine


class Corrector:
    """
    Check if correction is required:
    1.  Pos1

    """

    @staticmethod
    def correct_to_max(action: int, upper_limit: int) -> tuple[bool, int]:
        """
        1.  If action strictly-greater than (upper-) range, correct it
        2.  otherwise, leave as is

        :param action:
        :param upper_limit:
        :return:
        """

        if action > upper_limit:
            return True, upper_limit
        else:
            return False, action

    @staticmethod
    def correct_to_min(action: int, lower_limit: int) -> tuple[bool, int]:
        """
        1.  If action strictly-smaller than (lower-) range, correct it
        2.  otherwise, leave as is

        :param action:
        :param lower_limit:
        :return:
        """

        if action < lower_limit:
            return True, lower_limit
        else:
            return False, action

    @staticmethod
    def correct_within(action: int, limit: np.ndarray) -> tuple[bool, int]:
        """
        1.  if strictly greater or smaller than range, correct it
        2.  otherwise, leave as is

        :param action:
        :param limit:
        :return:
        """

        if action < limit[0]:
            return True, limit[0]
        elif action > limit[1]:
            return True, limit[1]
        else:
            return False, action


class Fetcher(ABC):
    """
    An interactor:
    1.  fetch the movements to feed to the engine

    Typically,
    1.  PRE-phase:
        1.  (rot, pos1)
    2.  MOVE-phase:
        1.  move

    """

    @staticmethod
    def pre_rot(engine: Engine, pre_rot: int):
        pass

    @staticmethod
    def pre_pos1_raw():
        pass

    @staticmethod
    def pos1_raw_maxout():
        """
        Correct pos1:
        1.  if exceeded boundary: apply maximal value

        :return:
        """

        pass

    @staticmethod
    def pos1_raw():
        """
        Do NOT correct pos1

        :return:
        """

        pass

    @staticmethod
    def pre(engine: Engine) -> tuple[int, int]:
        """
        The PRE-phase

        :param engine:
        :return:
        """

        pass

    @staticmethod
    def atomic(engine: Engine) -> tuple[int, int]:
        """

        :param engine:
        :return:
        """

        pass


def test_correct():
    print("correct to max")
    print(Corrector.correct_to_max(1, 2))
    print(Corrector.correct_to_max(3, 2))

    print("correct to min")
    print(Corrector.correct_to_min(1, 2))
    print(Corrector.correct_to_min(3, 2))

    print("correct to range")
    print(Corrector.correct_within(-1, np.array((0, 9))))
    print(Corrector.correct_within(0, np.array((0, 9))))
    print(Corrector.correct_within(4, np.array((0, 9))))
    print(Corrector.correct_within(9, np.array((0, 9))))
    print(Corrector.correct_within(11, np.array((0, 9))))


if __name__ == "__main__":
    pass
    test_correct()
