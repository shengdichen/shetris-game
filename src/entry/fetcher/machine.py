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
from src.entry.fetcher.human import _InputConverter


class FetcherMachine:
    """
    For Interacting with general machine-inputs

    """

    @staticmethod
    def pre_rot(engine: Engine, input_rot: int) -> tuple[int, np.ndarray]:
        valid_range_shifted = engine.mover.analyzer.get_shifted_range1(
            engine.piece.pid, input_rot
        )

        return input_rot, valid_range_shifted

    @staticmethod
    def pre_pos1(valid_range: np.ndarray):
        return _InputConverter.prompt_pre_pos1(valid_range)

    @staticmethod
    def pre(engine: Engine, input_rot: int) -> tuple[int, int]:
        pre_rot, valid_range = FetcherMachine.pre_rot(engine, input_rot)
        pre_pos1 = FetcherMachine.pre_pos1(valid_range)

        return pre_rot, pre_pos1


if __name__ == "__main__":
    pass
