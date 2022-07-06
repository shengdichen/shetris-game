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

    @staticmethod
    def prompt_pre() -> tuple[int, int]:
        """
        Ask for the pre-move:
        1.  (rot, pos1)

        :return:
        """

        move_input = input("Give me the pre-move: (delta_rot <space> delta_pos1)")
        if move_input:
            delta_rot, delta_pos1 = _InputConverter._string_to_ints(move_input)
            return delta_rot, delta_pos1
        else:
            return 0, 0

    @staticmethod
    def prompt_atomic() -> Optional[tuple[int, bool]]:
        """
        1.  Expect input of form (type, pos_dir):
            a.  type: 0 if in pos0, 1 if in pos1, anything else for rot
            b.  pos_dir: 1 if True; 0 if False
        2.  Translate it to a tuple

        :return:
        """

        move_input = input("Give me the atomic: (move_type <space> pos_dir)")
        if move_input:
            move_type, pos_dir = _InputConverter._string_to_ints(move_input)
            return move_type, bool(pos_dir)
        else:
            return None

    @staticmethod
    def prompt_multi() -> Optional[tuple[int, int]]:
        """
        1.  Expect input of form (type, delta):
            a.  type: 0 if in pos0, 1 if in pos1, anything else for rot
            b.  delta: the amount of shift (positive value for shift in
            positive-direction,
            negative value otherwise)
        2.  Translate it to a tuple.

        NOTE:
        Now all information is available to call the mover-function for a
        multi.

        :return:
        """

        move_input = input("Give me the multi: (move_type <space> delta)")
        if move_input:
            move_type, delta = tuple(map(int, move_input.split()))
            return move_type, delta
        else:
            return None


def input_converter_test():
    ic = _InputConverter

    print(ic.prompt_pre_rot())
    print(ic.prompt_pre_pos1(np.array((1, 9))))

    print(ic.prompt_pre())
    print(ic.prompt_atomic())
    print(ic.prompt_multi())


class FetcherTerminal:
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
        pass

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

        pre_rot = _InputConverter.prompt_pre_rot()

        pre_rot, valid_range = FetcherTerminal.pre_rot(engine)
        pre_pos1 = FetcherTerminal.pre_pos1(valid_range)

        return pre_rot, pre_pos1

    @staticmethod
    def

    @staticmethod
    def pre_default(engine: Engine):
        """
        Execute the pre-move: (0, 0)

        :return:
        """

        engine.init_piece()

        engine.exec_pre(0, 0)

        print("Engine done: pre")

    @staticmethod
    def pre_terminal(engine: Engine):
        """
        1.  Obtain the pre-move from terminal
        2.  Execute it

        :return:
        """

        engine.init_piece()

        analyzer = engine.mover.analyzer
        pre = _InputConverter.prompt_pre()
        if pre is not None:
            delta_rot, delta_pos1 = pre

            piece = engine.piece

            limit_low = analyzer.get_valid_range(
                piece.pid, piece.config.rot, False, False
            )
            limit_high = analyzer.get_valid_range(
                piece.pid, piece.config.rot, False, True
            )
            print("Valid range: ({0}, {1})".format(limit_low, limit_high))

            engine.exec_pre(delta_rot, delta_pos1)

        print("Engine done: pre")

    @staticmethod
    def multi_terminal(engine: Engine):
        multi = _InputConverter.prompt_multi()
        if multi is not None:
            move_type, delta = multi
            engine.exec_multi(move_type, delta)

        print("Engine done: multi")


if __name__ == "__main__":
    pass
    # input_converter_test()
