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


class FreezePhase:
    """
    Freeze-phase:
    1.  start: user's input is over to move piece
    2.  end: update to the field

    NOTE:
    1.  the drop is NOT in move-phase:
        ->  in FREEZE-phase instead

    """

    @staticmethod
    def with_drop(engine: Engine) -> list[np.ndarray]:
        """
        1.  drop
        2.  freeze

        Usage:
        1.  the more traditional game

        :return:
        """

        engine.exec_drop()
        return engine.exec_freeze()

    @staticmethod
    def without_drop(engine: Engine) -> list[np.ndarray]:
        """
        1.  do not drop, just freeze

        Usage:
        1.  for "floaty" pieces

        :return:
        """

        return engine.exec_freeze()


class FreezePhaseGym:
    """
    In the gym-type setup, the init-piece is relocated to FREEZE-phase
    (instead of the PRE-phase)

    """

    @staticmethod
    def with_drop(engine: Engine) -> list[np.ndarray]:
        """
        1.  drop
        2.  freeze

        Usage:
        1.  the more traditional game

        :return:
        """

        engine.exec_drop()
        line_chunks = engine.exec_freeze()

        engine.init_piece()
        return line_chunks


if __name__ == "__main__":
    pass
