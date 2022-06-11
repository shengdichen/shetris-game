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

    @property
    def field(self):
        return self._field

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

        if self._failed_boundaries_collision(check_string, piece_new.coord):
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

        if self._failed_boundaries_collision(check_string, piece_new.coord):
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
            if not self._failed_boundaries_collision("LRUD", piece_new.coord):
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
