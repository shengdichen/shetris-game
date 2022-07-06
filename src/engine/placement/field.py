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

from src.util.idxfac import IndexFactory


class Field:
    """
    The field must be able to do:
    1.  Indexing:
        Give me coords,
        Tell you the values there.
    2.  Checks:
        Give me coords,
        Tell you if exceeded boundaries or has collision.
    3.  Line-Clear operation
        Given me nothing,
        Remove full lines, shift everything above that downwards
        This includes the following operations:
        a.  report full rows;
        b.  report indexes of non-zero entries
        c.  write to new values based on np's (advanced-)indexing
    4.  Write-backs:
        Given me coords (checked: no exceeding boundaries, no collisions)
        Write True back to the field in these coords.

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

    @field.setter
    def field(self, value: np.ndarray):
        self._field = value

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

    def _full_row_num(self, target_range: tuple[int, int]) -> Optional[np.ndarray]:
        """
        Find numbers (indexes) of all full rows.

        NOTE:
            The output of this is not necessarily consecutive:
            E.g.: an I-piece (bar-piece) could have the top and the bottom of
            its four boxes in a full-row, while some of its two rows in between
            are not full.

        NOTE:
            The indexing convention of numpy and range() is used for the input:
            E.g.: if want to target the lines of (15, 16, 17), then this
            range-value should be (15, 18).
            E.g.: if want to target the whole field, this should be: (0,
            self.size[0]).

        :param target_range: (Continuous) range of rows to look for full-rows
        within.
        :return: indexes (1D np.ndarray) of full-rows.
        """

        lower_than, higher_than = target_range
        target_field = self.field[lower_than:higher_than, :]

        # a vector of n_rows: True if a row is full, False otherwise
        is_fullrow = np.all(target_field, axis=1)
        # nonzero() returns a tuple for np's advanced indexing: fish out with
        # [0]
        fullrow_numbers = np.nonzero(is_fullrow)[0]
        # print(fullrow_numbers)

        if fullrow_numbers.size == 0:
            return None
        # must add back the starting position if we did not look at the whole
        # field
        return fullrow_numbers + lower_than

    def idx_nonzero(self, higher_than: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Get numpy-indexes of non-zero boxes, if a range is provided (a tuple),
        use this for slicing.

        :param higher_than: typically: above_row is the highest row to be
        cleared next
        :return: numpy-indexes of non-zero entries
        """

        if higher_than is None:
            # 0-indexing
            #   -> this is one row BELOW the lowest row of the field
            #   -> look at the whole field!
            higher_than = self.size[0]
        field_view = self.field[:higher_than, :]

        idx_view = np.nonzero(field_view)
        return idx_view

    def set_from_idx(self, idx: tuple[np.ndarray, np.ndarray], new_val: bool):
        """
        Set entries at provided numpy-indexes to new value.

        :param idx:
        :param new_val:
        :return:
        """

        self.field[idx] = new_val

    def set_from_idx_pair(
        self,
        idx_old: tuple[np.ndarray, np.ndarray],
        idx_new: tuple[np.ndarray, np.ndarray],
    ):
        self.set_from_idx(idx_old, False)
        self.set_from_idx(idx_new, True)

    def lineclear(self, span_of_piece: Optional[np.ndarray] = None) -> list[np.ndarray]:
        """
        Perform the OP-LINECLEAR:
        1.  find full-rows
            a.  Considering the fact that this is usually called after a piece
            has finished moving, the (optional) argument indicates the vertical
            range of this newly finished piece.
            b.  in the absence of this span, the whole field is targeted
        2.  if there are no lines to clear:
            ->  return immediately
        3.  if there are full lines:
            ->  break them into consecutive chunks (routine defined below)
            ->  from the highest (lowest index in np) chunk to the lowest:
                ->  perform line-clear on each chunk (routine defined below)

        Return a list of all such chunks if existent, empty list otherwise

        NOTE:
        1.  the (vertical) span of a piece must be provided as:
            (upper_row_of_piece, lower_row_of_piece + 1)
            in the usual range() convention of numpy and python

        :type span_of_piece: the vertical span to target
        :return: all chunks of full lines if existent, empty list otherwise
        """

        if span_of_piece is None:
            # 0-indexing:
            #   -> this is one row BELOW the lowest row of the field
            #   -> look at the whole field!
            target_range = 0, self.size[0]
        else:
            target_range = span_of_piece

        full_rows = self._full_row_num(target_range)
        if full_rows is not None:
            chunks = Field._break_into_chunks(full_rows)
            for chunk in chunks:
                self._lineclear_chunk(chunk)
        else:
            chunks = []

        return chunks

    @staticmethod
    def _break_into_chunks(all_lines: np.ndarray) -> list[np.ndarray]:
        """
        Utility to break indexes of all full lines into consecutive chunks.


        The input (all_liens) is supposed to be:
        0.  all integers
        1.  strictly increasing (as is the result when querying full-lines)
        2.  not empty (containing at least one element)

        E.g.,
        [IN]
            all_lines = np.array([1, 2, 3, 4, 6, 7, 9, 11])
        [OUT]
            [array([1, 2, 3, 4]), array([6, 7]), array([9]), array([11])]
        [IN]
            all_lines = np.array([1])
        [OUT]
            [array([1])]

        :param all_lines: indexes of all full lines.
        :return: a list of np.ndarrays, each a consecutive sequence of
        index(es).
        """

        curr = np.array((all_lines[0],))
        chunks = []

        for idx in all_lines[1:]:
            if idx == curr[-1] + 1:
                curr = np.append(curr, idx)
            else:
                chunks.append(curr)

                curr = np.array((idx,))

        # must manually add the last chunk
        chunks.append(curr)

        return chunks

    def _set_rows(self, rows: np.ndarray, new_val=False) -> None:
        """
        Set all row-numbers into new value.

        :param rows: the rows to set
        :param new_val: the value to set them to
        """

        self.field[(rows,)] = new_val

    def _lineclear_chunk(self, chunk: np.ndarray) -> None:
        """
        Perform line-clear within a chunk of consecutive lines.

        NOTE:
        It is up to the caller to guarantee that chunk is not empty, i.e.,
        there is at least one line to clear.

        1.  set all rows of the chunk to 0;
        2.  move everything (strictly) above the top of the chunk downwards

        :return:
        """

        self._set_rows(chunk, False)
        higher_than, n_full_rows = np.min(chunk), chunk.shape[0]

        idx_nonzero = self.idx_nonzero(higher_than)
        idx_new = IndexFactory.make_shifted_pos0(idx_nonzero, n_full_rows)
        self.set_from_idx_pair(idx_nonzero, idx_new)

    def _set_one(self, coord: np.ndarray, new_val: bool = True) -> None:
        """
        Set one entry at some coord to some new value.

        :param coord:
        :param new_val:
        """

        self.field[self.unpack_coord(coord)] = new_val

    def set_many(self, coords: np.ndarray, new_val: bool = True) -> None:
        """
        Set all entries at provided coords to the (same) new value.

        Usage:
        1.  after a piece has finished moving, write its final coordinates to
        the field before envoking the line-clear.

        :param coords:
        :param new_val:
        """

        for coord in coords:
            self._set_one(coord, new_val)


def run_field_init():
    from src.util.fieldfac import FieldReader

    f = Field(FieldReader.read_from_file())
    f.print_field()


def run_boundary_checks():
    from src.util.fieldfac import FieldReader

    f = Field(FieldReader.read_from_file())

    print("LR-checks")
    print(f.exceeded_boundaries("L", np.array(((+0, +0), (+0, -1)))) is True)
    print(f.exceeded_boundaries("L", np.array(((+0, +0), (+0, +0)))) is False)
    print(f.exceeded_boundaries("R", np.array(((+0, +0), (+0, 10)))) is True)
    print(f.exceeded_boundaries("R", np.array(((+0, +0), (+0, 9)))) is False)

    print("UD-checks")
    print(f.exceeded_boundaries("U", np.array(((+0, +0), (-1, +0)))) is True)
    print(f.exceeded_boundaries("U", np.array(((+0, +0), (+0, +0)))) is False)
    print(f.exceeded_boundaries("D", np.array(((+0, +0), (+20, +0)))) is True)
    print(f.exceeded_boundaries("D", np.array(((+0, +0), (+19, +0)))) is False)

    print("mix-checks")
    print(f.exceeded_boundaries("R", np.array(((+0, +0), (+0, -1)))) is False)
    print(f.exceeded_boundaries("L", np.array(((+0, +0), (+0, -1)))) is True)
    print(f.exceeded_boundaries("L", np.array(((+0, +0), (+0, 10)))) is False)
    print(f.exceeded_boundaries("R", np.array(((+0, +0), (+0, 10)))) is True)


def run_collision_checks():
    from src.util.fieldfac import FieldReader

    f = Field(FieldReader.read_from_file())

    print("collision checks")
    # has collision (we have a piece at (+1, +1))
    print(f.has_collision(np.array(((+1, +0), (+1, +1), (+1, +2), (+1, +3)))))
    print(f.has_collision(np.array(((+1, +1), (+1, +2), (+1, +3), (+1, +4)))))
    print(not f.has_collision(np.array(((+1, +2), (+1, +3), (+1, +4), (+1, +5)))))


def run_lineclear():
    from src.util.fieldfac import FieldReader

    f = Field(FieldReader.read_from_file("lineclear/sample"))
    f.print_field()

    print("simulate line-clear")
    print(f.lineclear(None)[0].size)

    f.print_field()


def run_writeback_checks():
    from src.util.fieldfac import FieldReader

    f = Field(FieldReader.read_from_file())

    print("simulate initial coord")
    # the initial coord (after pid-generation and initial-move)
    coords = np.array(((+1, +2), (+1, +3), (+1, +4), (+1, +5)))
    f.set_many(coords)
    f.print_field()


if __name__ == "__main__":
    run_lineclear()
    pass
