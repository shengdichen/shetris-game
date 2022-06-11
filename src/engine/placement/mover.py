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

    def attempt_multi(
        self, move_type: int, piece: Piece, delta: int
    ) -> Optional[Piece]:
        """
        Perform multi-move (multiple atomics of the same move type):
        1.  which type of atomic;
        2.  current piece-info;
        3.  how many of such atomics are performed
        This is used for bot-plays.

        NOTE:
        if the multi failed after any amount of atomic, fail the multi
        completely, i.e., the state before the fail is NOT returned.

        :param move_type: 0 for pos0, 1 for pos1; anything else for rot
        :param piece: current piece-info
        :param delta: signed integer:
            i.  positive value for move in positive direction;
            ii. negative value for move in negative direction.
        :return:
        """

        positive_dir, delta = Mover.multi_to_dir_delta(delta)

        if move_type == 0:
            atomic_mover = self.attempt_atomic_pos0
        elif move_type == 1:
            atomic_mover = self.attempt_atomic_pos1
        else:
            atomic_mover = self.attempt_atomic_rot

        for __ in range(delta):
            result = atomic_mover(piece, positive_dir)
            if result is None:
                return None
            else:
                piece = result

        return piece

    def attempt_maxout(self, move_type: int, piece: Piece, pos_dir: bool) -> Piece:
        """
        Perform one atomic until failing. One special case of this is the
        hard-drop.

        NOTE:
        It is up to the user to assume that the initial state is legal, i.e.,
        before performing this max-out move, no exceeded boundaries or
        collision.

        NOTE:
        This operation always returns a 'Piece': even if no atomic can be
        performed at all, it will just return the passed-in piece-info, which,
        per the previous NOTE, is by definition valid.

        :param move_type: 0 for pos0, 1 for pos1; anything else for rot
        :param piece: current piece-info
        :param pos_dir: True for move in positive-direction, False otherwise
        :return:
        """

        if move_type == 0:
            atomic_mover = self.attempt_atomic_pos0
        elif move_type == 1:
            atomic_mover = self.attempt_atomic_pos1
        else:
            atomic_mover = self.attempt_atomic_rot

        maxed_out = False
        while not maxed_out:
            result = atomic_mover(piece, pos_dir)
            if result is None:
                maxed_out = True
            else:
                piece = result

        return piece

    def attempt_drop(self, piece: Piece) -> Piece:
        """
        A razor-thin wrapper to call the max-out operation on pos0, in positive
        direction;

        NOTE:
        Otherwise known as a "hard-drop".

        :param piece:
        :return:
        """

        return self.attempt_maxout(0, piece, True)

    def attempt_pre(
        self, piece: Piece, delta_rot: int, delta_pos1: int
    ) -> Optional[Piece]:
        """
        Conclude the PRE-phase after the new pid is available and piece-info
        is generated from the initial (-4, 0, 0)-config. Specifically:
        1.  apply user's rot to the initial, (-4, 0, 0)-config:
            ->  boundary-checks: by definition of rotation, still out of the
            "Up"-boundary (and still within "Left", "Right" and "Down")
            ->  collision-checks: no collision apparently, since out of field
        2.  given the piece and the rot, fetch and set to its ZERO-pos:
            ->  the vertical pos0 is frozen until end of PRE-phase, the
            horizontal pos1 is still manoeuvrable
            ->  per definition of the zero-pos, this is now within all
            boundaries
            ->  might still collide, but deliberately not checked just now to
            allow user's pos1 input of the next step
        3.  apply user's input pos1 to the now ZERO-pos:
            ->  finally, perform the "Left", "Right" boundary and collision
            checks
            ->  no need to check "Up" and "Down" in boundary, since the pos0
            from ZERO-pos has not been modified

        In short:
        1.  apply user's rotation-input
        2.  retrieve the zero position
        3.  apply user's pos1-input
        4.  check boundaries and collision

        NOTE:
        1.  should be called shortly after init_piece()
        2.  the passed in argument of the init-pos does not necessarily have to
        be (-4, 0):
            ->  it will be set to the ZERO-pos anyway

        :type piece: the piece with newly generated pid and (4, 0, 0)-config
        :param delta_pos1: multi-move delta in pos1 of PRE-phase
        :param delta_rot: multi-move delta in rot of PRE-phase
        :return: result of the move of PRE-phase
        """

        if not delta_rot == 0:
            piece = Piece.from_multi_rot(piece, delta_rot)

        zero_pos = self.analyzer.get_zero_pos(piece.pid, piece.config.rot)
        piece = Piece.to_absolute_pos(piece, zero_pos)
        # print("Piece in ZERO-pos:", piece)

        if not delta_pos1 == 0:
            piece = Piece.from_multi_pos1(piece, delta_pos1)

        if self.bad_boundaries_collision("LR", piece):
            return None
        return piece

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

    def get_zero_pos(self, pid: int, rot: int) -> np.ndarray:
        """
        Get the:
        1.  Up-most
        2.  AND left-most
        reference-pos for a piece in some rotation, referred to as the
        "ZERO"-ref-pos.

        NOTE:
        The knowledge of this particular "ZERO" ref-pos is critical for the
        PRE-phase:
        1.  after pid has been generated, and user's input for rot for the
        pre-phase has been processed
        2.  before the user's input for pos1 is processed

        NOTE:
        Significance of the ZERO-pos:
        1.  Once a piece is in zero-pos, the immediately following input of:
                SHIFT in pos0 and pos1
            is exactly equal to the resultant
                ABSOLUTE-VALUE in pos0 and pos1
            subject of course to subsequent boundary & collision checks
        2.  As a consequence, the
                static(!) valid-range of the ref-pos
            of this piece in this rot, as provided by the SRS-data, is directly
            equal to the
                valid INPUT range
        As a result, setting a piece to the ZERO-pos literally sets the pos of
        a piece to its (additive) 0-position, such that subsequent shift inputs
        (in pos) equates to the final, absolute state (in pos).

        :param pid:
        :param rot:
        :return:
        """

        if pid == 0:
            valid_range_all = self.valid_range_o[rot]
        elif pid == 1:
            valid_range_all = self.valid_range_i[rot]
        else:
            valid_range_all = self.valid_range_szljt[rot]

        return np.array((valid_range_all[0][0], valid_range_all[1][0]))

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


def analyzer_zero_pos_test():
    ba = BoundaryAnalyzer((20, 10))

    print("O-piece")
    print(ba.get_zero_pos(0, 0))
    print(ba.get_zero_pos(0, 1))
    print(ba.get_zero_pos(0, 2))
    print(ba.get_zero_pos(0, 3))

    print("I-piece")
    print(ba.get_zero_pos(1, 0))
    print(ba.get_zero_pos(1, 1))
    print(ba.get_zero_pos(1, 2))
    print(ba.get_zero_pos(1, 3))

    print("szljt-piece")
    print(ba.get_zero_pos(2, 0))
    print(ba.get_zero_pos(2, 1))
    print(ba.get_zero_pos(2, 2))
    print(ba.get_zero_pos(2, 3))


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


def boundary_test():
    m, piece = test_setup()
    m.field.print_field()

    # Right, within boundary
    piece = Piece.to_absolute_pos(piece, np.array((0, 6)))
    print(piece)
    print(m.bad_boundaries_collision("DURL", piece))
    # Right, OUTSIDE boundary
    piece = Piece.to_absolute_pos(piece, np.array((0, 7)))
    print(piece)
    print(m.bad_boundaries_collision("DURL", piece))

    # LEFT, within boundary
    piece = Piece.to_absolute_pos(piece, np.array((5, 0)))
    print(piece)
    print(m.bad_boundaries_collision("DURL", piece))

    # LEFT, OUTSIDE
    piece = Piece.to_absolute_pos(piece, np.array((5, -1)))
    print(piece)
    print(m.bad_boundaries_collision("DURL", piece))

    # NOTE:
    # the following code demonstrates direct usage of boundary-checks, avoid if
    # possible as the boundary-collision check short-circuits with the
    # boundary-checks performed first anyway
    #
    # # Up, within boundary
    # Piece.to_absolute_pos(piece, np.array((-1, 0)))
    # print(piece)
    # print(m._bad_boundary(piece, True, False))
    # # Up, OUTSIDE boundary
    # piece = Piece.to_absolute_pos(piece, np.array((-2, 0)))
    # print(piece)
    # print(m._bad_boundary(piece, True, False))
    #
    # # Down, within boundary
    # piece = Piece.to_absolute_pos(piece, np.array((18, 0)))
    # print(piece)
    # print(m._bad_boundary(piece, True, True))
    # # Up, OUTSIDE boundary
    # piece = Piece.to_absolute_pos(piece, np.array((19, 0)))
    # print(piece)
    # print(m._bad_boundary(piece, True, True))


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


def multi_test():
    m, piece = test_setup()
    m.field.print_field()
    print(piece)

    print("Checking multi")
    # these two will succeed
    piece = m.attempt_multi(1, piece, 5)
    piece = m.attempt_multi(0, piece, 2)
    print(piece)

    # this will fail, printing nothing (None)
    print(m.attempt_multi(1, piece, -4))


def maxout_test():
    m, piece = test_setup()
    m.field.print_field()

    piece = m.attempt_multi(1, piece, 3)
    piece = m.attempt_multi(0, piece, 1)
    print("Initial position:", piece)

    piece = m.attempt_maxout(1, piece, False)
    print("left maxout:", piece)

    piece = m.attempt_maxout(1, piece, True)
    print("right maxout:", piece)
    # attempting the same maxout should not change anything
    print("right maxout, again:", m.attempt_maxout(1, piece, True))

    # hard-drop
    piece = m.attempt_maxout(0, piece, True)
    print("hard-drop:", piece)


def premove_test():
    from src.engine.placement.piece import Config

    m, piece = test_setup()
    m.field.print_field()

    # this will fail
    pid = 6
    config = Config(np.array([-4, +0]), 0)
    piece = Piece.from_init(pid, config)
    print(m.attempt_pre(piece))

    # this will also fail
    pid = 6
    config = Config(np.array([-4, +1]), 0)
    piece = Piece.from_init(pid, config)
    print(m.attempt_pre(piece))

    # this will succeed
    pid = 6
    config = Config(np.array([-4, +2]), 0)
    piece = Piece.from_init(pid, config)
    print(m.attempt_pre(piece))

    # this is to check that pre-move does not over-drop: stops dropping
    # immediately after all four boxes are in-field
    pid = 6
    config = Config(np.array([-4, +3]), 0)
    piece = Piece.from_init(pid, config)
    print(m.attempt_pre(piece))

    # another non-over-drop test
    pid = 6
    config = Config(np.array([-4, +5]), 0)
    piece = Piece.from_init(pid, config)
    print(m.attempt_pre(piece))


if __name__ == "__main__":
    pass
