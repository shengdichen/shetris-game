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


class _InputConverter:
    """
    Give me:
    1.  human's random input at terminal
    And I will:
    1.  convert this input to a tuple of integers

    """

    @staticmethod
    def _string_to_ints(move_input: str):
        """
        Common operation:
        split a string (from user's input) into many ints

        :param move_input:
        :return:
        """

        return tuple(map(int, move_input.split()))

    @staticmethod
    def prompt_pre_rot() -> int:
        move_input = input("Give me the pre-rot: (delta_rot)")
        if move_input:
            return _InputConverter._string_to_ints(move_input)[0]
        else:
            return 0

    @staticmethod
    def prompt_pre_pos1(valid_range: np.ndarray) -> int:
        move_input = input(
            "Give me the pre-pos1: (delta_pos1) within {0}".format(valid_range)
        )
        if move_input:
            return _InputConverter._string_to_ints(move_input)[0]
        else:
            return 0


def input_converter_test():
    ic = _InputConverter

    print(ic.prompt_pre_rot())
    print(ic.prompt_pre_pos1(np.array((1, 9))))


class InteractorTerminal:
    """
    Handle all the pre-processing between:
    1.  a human's input to terminal
    2.  the engine
    in the raw, prompt-and-type fashion.

    """

    @staticmethod
    def pre_rot(engine: Engine) -> tuple[int, np.ndarray]:
        """
        First part (of two) of the PRE-phase:
        1.  Fetch the rot from input
        2.  Get the resultant pos1-limit
            ->  shifted to (0, *), i.e., always non-negative

        :param engine:
        :return: the pre-rot and the valid-range
        """

        pre_rot = _InputConverter.prompt_pre_rot()

        valid_range_shifted = engine.mover.analyzer.get_shifted_range1(
            engine.piece.pid, pre_rot
        )

        return pre_rot, valid_range_shifted

    @staticmethod
    def pre_pos1(valid_range: np.ndarray) -> int:
        """
        Second part (of two) of the PRE-phase:
        1.  Fetch the pos1 from input

        :param valid_range:
        :return:
        """

        return _InputConverter.prompt_pre_pos1(valid_range)

    @staticmethod
    def pre(engine: Engine) -> tuple[int, int]:
        """
        The PRE-phase

        :param engine:
        :return:
        """

        pre_rot, valid_range = InteractorTerminal.pre_rot(engine)
        pre_pos1 = InteractorTerminal.pre_pos1(valid_range)

        return pre_rot, pre_pos1


if __name__ == "__main__":
    pass
