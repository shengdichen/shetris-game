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


from abc import ABC, abstractmethod

import numpy as np


class GUI(ABC):
    """
    A field-front should support:
    1.  pull-in front a matrix
    This really is the only thing that is absolutely required: the engine does
    the processing of placing a piece, the GUI just needs to be able to paint:
        1.  all boxes of TRUE to some color
        2.  all boxes of FALSE to another color

    2.  set from some coords: when a piece's pid is initially generated and its
    initial coordinates are found:
        1.  This should set (usually four boxes) to some active-color (might be
        just color for all TRUE boxes)

    3.  update from a pair of coordinates (coord_old, coord_new) after an
    atomic:
        1.  paint coord_old to color-FALSE
        2.  paint coord_new to color-TRUE

    What should NOT be handled by a field-front:
    1.  setting a line:
        1.  this operation happens at the operation line-clear;
        2.  the operation line-clear itself shall be performed by the
        placement;
        3.  the field-front should instead use the read-from-matrix
        functionality to update the front, once the placement delivers the
        post-clear result.

    """

    def __init__(self, field):
        """
        init the underlying field matrix
        """
        self._field = field

    @abstractmethod
    def read_from_field(self, field):
        """
        read directly from the field (np.array)

        Usage:
            1. human-mode: after a lock (take into account of line-clear)
            2. bot-mode: after every bot-move

        :param field:
        :return:
        """

        pass

    @abstractmethod
    def set_from_idx(self, idx: tuple[np.ndarray, np.ndarray], new_state: bool):
        """
        Called when a piece is initially created.

        :param idx:
        :param new_state:
        :return:
        """

        pass

    @abstractmethod
    def set_from_pair(self, idx_old, idx_new):
        """
        Called after every atomic:
        1.  set the idx_old to FALSE
        2.  set the idx_new to TRUE

        :param idx_old:
        :param idx_new:
        :return:
        """

        self.set_from_idx(idx_old, False)
        self.set_from_idx(idx_new, True)
