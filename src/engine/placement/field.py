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


class Field:
    """
    The field must be able to do:
    1.  Indexing:
        Give me coords,
        Tell you the values there.
    2.  Checks:
        Give me coords,
        Tell you if exceeded boundaries or has collision.

    """

    # format:
    # "check_string": [checking_in_pos0, checking_in_pos_dir]
    check_strings_to_internals = {
        "U": [True, False],
        "D": [True, True],
        "L": [False, False],
        "R": [False, True],
    }

    def __init__(self, field: np.ndarray):
        self._field = field
        self._size = field.shape

    @property
    def field(self):
        return self._field

    @property
    def size(self):
        return self._size

    def print_field(self):
        """
        print every entry as 1 or 0, instead of True or False,
        making for a nicely aligned field in terminal-output

        """

        def print_bool_as_int(my_bool):
            return str(int(my_bool))

        np.set_printoptions(formatter={"bool": print_bool_as_int})
        print(self.field)

        # reset printoptions
        np.set_printoptions()

    @staticmethod
    def unpack_coord(coord: np.ndarray) -> tuple[int, int]:
        """
        Problem:
            Accessing np.array with index of type np.array triggers np's
            internal advanced-indexing.
        Solution:
            Manually unpack a coord (np.array); use this for access. This
            routine performs this unpacking

        :param coord: one np.array coord (two-entry, 1D)
        :return: entry at the coord
        """

        return coord[0], coord[1]

    def at_one(self, coord: np.ndarray) -> bool:
        """
        Get the entry of at one coordinate of np.ndarray.

        :param coord: np.ndarray
        :return: the entry at the coord
        """
        return self.field[Field.unpack_coord(coord)]

    def at(self, coords: np.ndarray) -> np.ndarray:
        """
        Get the entries at many coordinates: a 2D np.ndarray:
        1.  each is a coordinate
        2.  i.e., dimension is n_coords*2

        :param coords: the queried coordinates
        :return: the entries at the queried coordinates
        """
        n_entries_queried = coords.shape[0]
        states = np.empty(n_entries_queried, dtype=bool)

        for i in range(n_entries_queried):
            curr_coord = coords[i]
            #   print(curr_coord)
            states[i] = self.at_one(curr_coord)

        return states

    def has_collision(self, candidates: np.ndarray) -> bool:
        """
        Check if any candidate-coordinates collides with the existing field.

        :param candidates: the candidate-coordinates
        :return: True if collision exists, False otherwise
        """

        curr_vals = self.at(candidates)

        return np.any(curr_vals)

    def _exceeded_boundary(
        self, in_pos0: bool, in_pos_dir: bool, candidates: np.ndarray
    ) -> np.bool_:
        """
        Check if any of the candidates-coordinates have exceeded one specific
        boundary of the four "walls".

        :param in_pos0: bool
            True if in pos0 (check vertically);
            False if in pos1 (check horizontally)
        :param in_pos_dir: True if in negative direction, False otherwise
        :param candidates: coordinates (2D!, we will extract the
        relevant 1D coords in method!)

        :return:
        """

        candidates_to_check = candidates[:, 0] if in_pos0 else candidates[:, 1]

        if in_pos_dir:
            np_checkers = (np.max, np.greater)
            if in_pos0:
                boundary = self.size[0] - 1
            else:
                boundary = self.size[1] - 1
        else:
            boundary = 0
            np_checkers = (np.min, np.less)

        def _check_util_1d(
            _candidates_1d: np.ndarray, _boundary: int, _np_checkers: tuple
        ) -> np.bool_:
            """
            check boundary against some boundary

            :param _candidates_1d: 1D np.array (all rows or all cols)
            :param _boundary:
            :param _np_checkers:
            :return:
            """

            worst_candidate = _np_checkers[0](_candidates_1d)
            return _np_checkers[1](worst_candidate, _boundary)

        return _check_util_1d(candidates_to_check, boundary, np_checkers)

    def exceeded_boundaries(
        self, boundaries_string: str, candidates: np.ndarray
    ) -> bool:
        """
        Boundary-checks for multiple boundaries.

        NOTE:
        Short-circuiting is performed: as soon as one boundary-check is failed,
        return immediately.

        :param boundaries_string: any subset of "LRUD"
        :param candidates:
        :return:
        """

        for check_string in boundaries_string:
            in_pos0, in_pos_dir = Field.check_strings_to_internals[check_string]
            exceeded_curr = self._exceeded_boundary(in_pos0, in_pos_dir, candidates)
            if exceeded_curr:
                return True

        return False


if __name__ == "__main__":
    pass
