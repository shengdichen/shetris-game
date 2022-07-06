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


from typing import Callable

from src.engine.engine import Engine


class PrePhase:
    """
    PRE-phase: from pid-generation to knowing if game-over:
    1.  init pid
    2.  perform pre-input

    NOTE:
    1.  it is NOT up to the phase-executor to apply modifications to the input
    2.  the phase-executor just executes the action
    3.  it is NOT up to the executor to check game-over:
        ->  should be done in entry to decide game-over implementations

    """

    @staticmethod
    def default(
        engine: Engine, action_generator: Callable[..., tuple[int, int]]
    ) -> None:
        """
        1.  directly apply the action

        :return:
        """

        engine.init_piece()

        pre_rot, pre_pos1 = action_generator()
        engine.exec_pre(pre_rot, pre_pos1)

    @staticmethod
    def correction_aware(
        engine: Engine, action_generator: Callable[..., tuple[bool, int, int]]
    ) -> bool:
        """
        1.  Apply the action with correction-aware generator
        2.  Return True if corrected

        :param engine:
        :param action_generator:
        :return:
        """

        engine.init_piece()

        corrected, pre_rot, pre_pos1 = action_generator()
        engine.exec_pre(pre_rot, pre_pos1)
        # print("Engine done: pre")

        return corrected


class PrePhaseGym:
    """
    For the Gym interface:
    1.  no state change is allowed before applying the action:
    2.  thus: the init-piece must be relocated to the Freeze-phase

    """

    @staticmethod
    def default(
        engine: Engine, action_generator: Callable[..., tuple[int, int]]
    ) -> None:
        """
        1.  directly apply the action

        :return:
        """

        # engine.init_piece()

        pre_rot, pre_pos1 = action_generator()
        engine.exec_pre(pre_rot, pre_pos1)

    @staticmethod
    def correction_aware(
        engine: Engine, action_generator: Callable[..., tuple[bool, int, int]]
    ) -> bool:
        """
        1.  Apply the action with correction-aware generator
        2.  Return True if corrected

        :param engine:
        :param action_generator:
        :return:
        """

        # engine.init_piece()

        corrected, pre_rot, pre_pos1 = action_generator()
        engine.exec_pre(pre_rot, pre_pos1)
        # print("Engine done: pre")

        return corrected


if __name__ == "__main__":
    pass
