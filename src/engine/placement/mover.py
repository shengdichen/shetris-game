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

from src.engine.placement.field import Field
from src.engine.placement.piece import Piece
from src.engine.placement.srs.coord import RelCoord
from src.engine.placement.srs.kick import Kick


class Mover:
    """
    Tell me a move:
    1.  atomic
    2.  multi
    and I will give you:
    1.  if successful: the new piece-info
    2.  if not: None, as a signal of failure

    """

    check_string_to_check_tuple = {
        "U": [True, False],
        "D": [True, True],
        "L": [False, False],
        "R": [False, True],
    }

    def __init__(self, field: Field) -> None:
        """
        Tell the Mover to use some field.

        :param field: the field to use
        """

        self._field = field
        self._analyzer = BoundaryAnalyzer(self.field.size)

    @property
    def field(self):
        return self._field

    @property
    def analyzer(self):
        return self._analyzer

    @staticmethod
    def _atomic_to_check_string(atomic_type: int, positive_dir: bool) -> str:
        """
        Get the boundary-check-string of an atomic:
        i.  if moving left: check left-boundary;
        ii. if moving right: check right-boundary;
        etc.
        Otherwise, check all boundaries

        :param atomic_type: 0 for pos0; 1 for pos1; anything else for rot
        :param positive_dir: True if the atomic is in negative sense; False
        otherwise
        :return:
        """

        if atomic_type == 0:
            if positive_dir:
                check_string = "D"
            else:
                check_string = "U"
        elif atomic_type == 1:
            if positive_dir:
                check_string = "R"
            else:
                check_string = "L"
        else:
            check_string = "LRUD"

        return check_string

    def _failed_boundaries_collision(
        self, check_string: str, candidates: np.ndarray
    ) -> bool:
        """
        Check if boundaries- or collision-checks failed.

        NOTE:
        This is our standard check for any move: both atomic and multi.

        NOTE:
        Short-circuiting is used: boundary-checks are performed first, then the
        collision check. Returns As soon as one check fails. This ordering is
        intentional: the field is expected to be generally unoccupied, thus,
        the chances of exceeding some boundary (or boundaries) are expected to
        be higher than that of producing a collision.

        :param check_string: which boundaries to check
        :param candidates: potential coordinates (usually 4 of a piece)
        :return: True if failed checks (bad candidates); False otherwise
        """

        if self.field.exceeded_boundaries(check_string, candidates):
            return True

        if self.field.has_collision(candidates):
            return True

        return False

    def _attempt_atomic_pos(
        self, piece: Piece, in_pos0: bool, positive_dir: bool
    ) -> Optional[Piece]:
        """
        Attempt an atomic in pos0 or pos1.
        1.  first convert an atomic to the cooresponding check-string
        2.  perform the boundary-collision check

        :param piece: initial piece-information
        :param in_pos0: True if atomic in pos0; False otherwise (pos1)
        :param positive_dir: True if moving in positive direction; False else
        :return: None if the move failed; the new coords if succeeded
        """

        if in_pos0:
            check_string = Mover._atomic_to_check_string(0, positive_dir)
            piece_new = Piece.from_atomic_pos0(piece, positive_dir)
        else:
            check_string = Mover._atomic_to_check_string(1, positive_dir)
            piece_new = Piece.from_atomic_pos1(piece, positive_dir)

        if self.bad_boundaries_collision(check_string, piece_new):
            return None
        return piece_new

    def attempt_atomic_pos0(self, piece: Piece, positive_dir: bool) -> Optional[Piece]:
        """
        Razor-thin wrapper to perform atomic-pos0.

        :param piece:
        :param positive_dir:
        :return:
        """

        return self._attempt_atomic_pos(piece, True, positive_dir)

    def attempt_atomic_pos1(self, piece: Piece, positive_dir: bool) -> Optional[Piece]:
        """
        Razor-thin wrapper to perform atomic-pos1.

        :param piece:
        :param positive_dir:
        :return:
        """

        return self._attempt_atomic_pos(piece, False, positive_dir)

    def attempt_atomic_rot(self, piece: Piece, positive_dir: bool) -> Optional[Piece]:
        """
        attempt an atomic-rot:
            1. if the atomic-rot is successful, return the new piece-info;
            2. else, try all the srs-shift candidates, which shall also return
            the new piece-info if one of the candidates are successful
            3. if both steps fail, return None to signal failure

        :param piece:
        :param positive_dir:
        :return: new piece-info if successful, None otherwise
        """

        check_string = Mover._atomic_to_check_string(2, positive_dir)

        piece_new = Piece.from_atomic_rot(piece, positive_dir)

        if self.bad_boundaries_collision(check_string, piece_new):
            return self._try_srs_shifts(piece_new, positive_dir)

        return piece_new

    def _try_srs_shifts(self, piece: Piece, positive_dir: bool) -> Optional[Piece]:
        """
        Check every SRS-shift candidate (in order) after initially failed
        atomic-rot; this can be broken down to:
            1. obtain all srs-shift candidates;
            2. check each candidate by applying the corresponding move,
            which is a composite-pos
            3. as soon as a successful candidate is found, return the new
            piece-info; if none of the candidates are acceptable, return None
            to signal failure

        :param piece: piece AFTER initial atomic-rot
        :param positive_dir: True if in positive dir; False otherwise
        :return: the new piece if found; None otherwise
        """
        pid = piece.pid
        rot = piece.config.rot
        srs_shifts = Kick.get_srs_candidates(pid, rot, positive_dir)

        for shift in srs_shifts:
            piece_new = Piece.from_multi_pos(piece, shift)
            if not self.bad_boundaries_collision("LRUD", piece_new):
                return piece_new

        return None

    def attempt_atomic(
        self, move_type: int, piece: Piece, pos_dir: bool
    ) -> Optional[Piece]:
        """
        A thin-wrapper for handling any type of atomic:
        1.  which type of atomic;
        2.  current piece-info;
        3.  in positive or negative dir
        This is used for human-plays.

        :param move_type: 0 for pos0, 1 for pos1; anything else for rot
        :param piece: current piece-info
        :param pos_dir: True if in positive-dir, False otherwise
        :return:
        """

        if move_type == 0:
            atomic_mover = self.attempt_atomic_pos0
        elif move_type == 1:
            atomic_mover = self.attempt_atomic_pos1
        else:
            atomic_mover = self.attempt_atomic_rot

        return atomic_mover(piece, pos_dir)

    @staticmethod
    def multi_to_dir_delta(delta: int) -> tuple[bool, int]:
        """
        Convert a delta-value to:
        1.  its sign
        2.  absolute-value
        For calling the corresponding atomic-functions

        :return: (pos_dir, abs-val of delta)
        """
        if delta > 0:
            positive_dir = True
        else:
            positive_dir = False
            delta = -delta

        return positive_dir, delta

    def _bad_boundary(self, piece: Piece, is_pos0: bool, pos_dir: bool) -> bool:
        """
        Check if one boundary has been exceeded.

        :param piece:
        :param is_pos0:
        :param pos_dir:
        :return: True if exceeded this boundary, False otherwise
        """

        relevant_pos_idx = 0 if is_pos0 else 1
        relevant_pos = piece.config.pos[relevant_pos_idx]

        limit = self.analyzer.get_valid_range(
            piece.pid, piece.config.rot, is_pos0, pos_dir
        )
        # print("boundary check: {0} VS {1}".format(relevant_pos, limit))

        if pos_dir:
            exceeded_boundary = relevant_pos > limit
        else:
            exceeded_boundary = relevant_pos < limit
        return exceeded_boundary

    def _bad_boundaries(self, piece: Piece, check_str: str) -> bool:
        """
        Check if multiple boundaries have been exceeded.

        :param piece:
        :param check_str: any subset of "DURL"
        :return:
        """

        for curr_check_str in check_str:
            # print("checking boundary {0}".format(curr_check_str))
            in_pos0, in_pos_dir = Mover.check_string_to_check_tuple[curr_check_str]
            exceeded_curr = self._bad_boundary(piece, in_pos0, in_pos_dir)
            if exceeded_curr:
                print("Failed at {0}".format(curr_check_str))
                return True

        return False

    def bad_boundaries_collision(self, check_str: str, piece: Piece):
        """
        Perform the standard check:
        1.  Boundaries check
        2.  collision check

        :param check_str:
        :param piece:
        :return:
        """

        if self._bad_boundaries(piece, check_str):
            return True
        if self.field.has_collision(piece.coord):
            print("Failed collision")
            return True

        return False


class BoundaryAnalyzer:
    """
    Give me:
    1.  a piece-info
    And I will give you:
    1.  Whether it's within the bound
    """

    # hard-coded data for the standard 20*10 game-field
    # ((minimum-allowed-pos0, maximum-pos0), (min-pos1, max-pos1))
    _std_valid_range_o = np.array(
        (
            ((+0, +18), (-1, +7)),
            ((+0, +18), (-1, +7)),
            ((+0, +18), (-1, +7)),
            ((+0, +18), (-1, +7)),
        )
    )

    _std_valid_range_i = np.array(
        (
            ((-1, +18), (+0, +6)),
            ((+0, +16), (-1, +8)),
            ((-2, +17), (+0, +6)),
            ((+0, +16), (-2, +7)),
        )
    )

    _std_valid_range_szljt = np.array(
        (
            ((+0, +18), (+0, +7)),
            ((+0, +17), (+0, +8)),
            ((-1, +17), (+0, +7)),
            ((+0, +17), (-1, +7)),
        )
    )

    def __init__(self, size: tuple[int, int]):
        self._size0, self._size1 = size

        if self.size0 == 20 and self.size1 == 10:
            self._valid_range_o = BoundaryAnalyzer._std_valid_range_o
            self._valid_range_i = BoundaryAnalyzer._std_valid_range_i
            self._valid_range_szljt = BoundaryAnalyzer._std_valid_range_szljt
        else:
            self._valid_range_o = self._get_valid_range_all(RelCoord.rel_range_o)
            self._valid_range_i = self._get_valid_range_all(RelCoord.rel_range_i)
            self._valid_range_szljt = self._get_valid_range_all(
                RelCoord.rel_range_szljt
            )

    @property
    def size0(self):
        return self._size0

    @property
    def size1(self):
        return self._size1

    @property
    def valid_range_o(self):
        return self._valid_range_o

    @property
    def valid_range_i(self):
        return self._valid_range_i

    @property
    def valid_range_szljt(self):
        return self._valid_range_szljt

    def _get_valid_range_all(self, rel_range: np.ndarray) -> np.ndarray:
        """
        Calculate the valid range of every piece in all rotations.

        :param rel_range:
        :return:
        """

        limits = np.array(((0, self.size0), (0, self.size1)))
        return limits - rel_range

    def get_valid_range(self, pid: int, rot: int, is_pos0: bool, pos_dir: bool):
        """
        Get the valid range of a piece, in the sense that it stays within
        the boundary of the field

        Usage:
        Check exceeded boundary with:
            pos0 in range0
            pos1 in range1


        :param pid:
        :param rot:
        :param is_pos0:
        :param pos_dir:
        :return:
        """

        if pid == 0:
            valid_range_all = self.valid_range_o[rot]
        elif pid == 1:
            valid_range_all = self.valid_range_i[rot]
        else:
            valid_range_all = self.valid_range_szljt[rot]

        idx_pos = 0 if is_pos0 else 1
        idx_dir = 1 if pos_dir else 0

        return valid_range_all[idx_pos][idx_dir]


def analyzer_boundary_test():
    from src.engine.placement.piece import Config, Piece

    pid = 4
    config = Config(np.array([10, 2]), 3)
    piece = Piece.from_init(pid, config)
    print(piece)

    pa = BoundaryAnalyzer((20, 10))

    # all the valid ranges
    print("valid-range o")
    print(pa.valid_range_o)
    print("valid-range i")
    print(pa.valid_range_i)
    print("valid-range others")
    print(pa.valid_range_szljt)

    # D
    print("Down")
    print(pa.get_valid_range(1, 0, True, True))
    print(pa.get_valid_range(1, 1, True, True))
    print(pa.get_valid_range(1, 2, True, True))
    print(pa.get_valid_range(1, 3, True, True))

    # U
    print("Up")
    print(pa.get_valid_range(1, 0, True, False))
    print(pa.get_valid_range(1, 1, True, False))
    print(pa.get_valid_range(1, 2, True, False))
    print(pa.get_valid_range(1, 3, True, False))

    # R
    print("Right")
    print(pa.get_valid_range(1, 0, False, True))
    print(pa.get_valid_range(1, 1, False, True))
    print(pa.get_valid_range(1, 2, False, True))
    print(pa.get_valid_range(1, 3, False, True))

    # L
    print("Left")
    print(pa.get_valid_range(1, 0, False, False))
    print(pa.get_valid_range(1, 1, False, False))
    print(pa.get_valid_range(1, 2, False, False))
    print(pa.get_valid_range(1, 3, False, False))


def test_setup():
    from src.util.fieldfac import FieldReader
    from src.engine.placement.piece import Config

    f = Field(FieldReader.read_from_file())
    m = Mover(f)

    print("checking initial-put")
    pid = 1
    config = Config(np.array([-1, +0]), 0)
    piece = Piece.from_init(pid, config)

    return m, piece


def atomic_test():
    m, piece = test_setup()
    m.field.print_field()
    print(piece)

    print("Checking atomics")
    # this is successful
    attempt = m.attempt_atomic_pos1(piece, True)
    if attempt is not None:
        piece = attempt
        print("Right move successful\n", "piece")
        print(piece)
    else:
        print("Right move failed")

    # this will fail
    attempt = m.attempt_atomic_pos0(piece, True)
    if attempt is not None:
        piece = attempt
        print("Down move successful")
        print(piece)
    else:
        print("Down move failed")


if __name__ == "__main__":
    pass
