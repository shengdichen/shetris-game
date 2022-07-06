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


import tkinter

from src.engine.engine import Engine
from src.entry.fetcher.human import FetcherTerminal
from src.entry.stepper.pre import PrePhase
from src.front.fronttk import FieldTK


class GameTk:
    """
    A complete front should:
    1.  define key=binds to perform various operations

    2.  define the entry-point
    """

    root = tkinter.Tk()

    def __init__(self, size: tuple[int, int]):
        self._engine = Engine(size)

        self._front = FieldTK(GameTk.root, size)
        self._coord, self._coord_new = None, None

        self.setups_tk()

    @property
    def engine(self):
        return self._engine

    @property
    def front(self):
        return self._front

    @property
    def coord(self):
        return self._coord

    @coord.setter
    def coord(self, value):
        self._coord = value

    @property
    def coord_new(self):
        return self._coord_new

    @coord_new.setter
    def coord_new(self, value):
        self._coord_new = value

    def setups_tk(self) -> None:
        """
        All the setups necessary for Tk:
        1.  Perform all the key-binds
        2.  Set the correct default focus (on the game-frontend)
        3.  Start the main-loop of Tk

        :return:
        """

        self.exec_keybinds()

        GameTk.root.title("Shetris")
        self.front.focus()

        GameTk.start_gui_loop()

    def exec_keybinds(self) -> None:
        """
        Bind all actions to some key:
        1.  the atomics
        2.  the hard-drop
        3.  the lock

        :return: None
        """

        r = GameTk.root

        r.bind("w", self.wrapper_set_from_upstream)

        r.bind("e", self.wrapper_pre_default)
        r.bind("r", self.wrapper_pre_terminal)

        r.bind("j", self.wrapper_atomic_pos0_pos)
        r.bind("k", self.wrapper_atomic_pos0_neg)
        r.bind("l", self.wrapper_atomic_pos1_pos)
        r.bind("h", self.wrapper_atomic_pos1_neg)
        r.bind("a", self.wrapper_atomic_rot_pos)
        r.bind("d", self.wrapper_atomic_rot_neg)

        r.bind("x", self.wrapper_multi)

        r.bind("<space>", self.wrapper_drop)
        r.bind("J", self.wrapper_maxout_down)
        r.bind("K", self.wrapper_maxout_up)
        r.bind("L", self.wrapper_maxout_right)
        r.bind("H", self.wrapper_maxout_left)

        r.bind("<Return>", self.wrapper_freeze)

        r.bind("q", self.wrapper_clean_up)
        # r.bind("f", self.wrapper_set_from_file)

    def _set_from_upstream(self):
        """
        Sync from upstream field.

        :return:
        """

        self.front.set_from_matrix(self.engine.field.field)

    def wrapper_set_from_upstream(self, __):
        self._set_from_upstream()

    def _pre(self, use_zero: bool):
        """
        Execute the pre-move.

        :param use_zero: True to use the default (-4, 0, 0) before pre-move, False
        to get input
        :return:
        """

        if use_zero:
            PrePhase.apply_zero(self.engine)
        else:
            PrePhase.apply_hinted_corrected(self.engine)

        if self.engine.is_game_over:
            self._clean_up()

        self.coord = self.engine.piece.coord
        self.front.set_from_coords(self.coord, self.front.cl_coord_active)

    def wrapper_pre_default(self, *__):
        self._pre(True)

    def wrapper_pre_terminal(self, *__):
        self._pre(False)

    def _atomic(self, move_type: int, pos_dir: bool):
        """
        The core fetcher for key-binds for executing atomics

        :param move_type: 0 for pos0, 1 for pos1, anything else for rot
        :param pos_dir: True if positive
        :return:
        """

        self.coord = self.engine.piece.coord
        self.engine.exec_atomic(move_type, pos_dir)
        print("Engine done: multi")
        self.coord_new = self.engine.piece.coord

        self.front.set_from_pair((self.coord, self.coord_new))

    def wrapper_atomic_pos0_pos(self, __):
        self._atomic(0, True)

    def wrapper_atomic_pos0_neg(self, __):
        self._atomic(0, False)

    def wrapper_atomic_pos1_pos(self, __):
        self._atomic(1, True)

    def wrapper_atomic_pos1_neg(self, __):
        self._atomic(1, False)

    def wrapper_atomic_rot_pos(self, __):
        self._atomic(2, True)

    def wrapper_atomic_rot_neg(self, __):
        self._atomic(2, False)

    def _multi(self):
        self.coord = self.engine.piece.coord

        FetcherTerminal.multi_terminal(self.engine)
        self.coord_new = self.engine.piece.coord

        self.front.set_from_pair((self.coord, self.coord_new))

    def wrapper_multi(self, __):
        self._multi()

    def _drop(self):
        self.coord = self.engine.piece.coord

        # self.engine.piece = self.engine.mover.attempt_drop(self.engine.piece)
        self.engine.exec_drop()
        print("Engine done: drop")
        self.coord_new = self.engine.piece.coord

        self.front.set_from_pair((self.coord, self.coord_new))

    def _maxout(self, move_type: int, pos_dir: bool):
        self.coord = self.engine.piece.coord

        self.engine.exec_maxout(move_type, pos_dir)
        print("Engine done: multi")
        self.coord_new = self.engine.piece.coord

        self.front.set_from_pair((self.coord, self.coord_new))

    def wrapper_drop(self, __):
        self._drop()

    def wrapper_maxout_down(self, __):
        self._maxout(0, True)

    def wrapper_maxout_up(self, __):
        self._maxout(0, False)

    def wrapper_maxout_right(self, __):
        self._maxout(1, True)

    def wrapper_maxout_left(self, __):
        self._maxout(1, False)

    def _freeze(self):
        """
        Due to the absence of a real loop when dealing with Tk, ending a piece means:
        1.  calling engine's freeze (apparently)
        2.  sync from engine's upstream field (apparently)
        3.  spawn the new piece (to also start the next sequence, i.e., we are manually
        creating the loop)

        :return:
        """

        self._drop()
        self.engine.exec_freeze()
        print("Engine done: Piece Finish")

        self._set_from_upstream()

        # self._pre(False)

    def wrapper_freeze(self, __):
        self._freeze()

    def _set_from_file(self):
        """
        1.  Test key-bind of Tk
        2.  Display our test field

        :return:
        """

        from src.util.fieldfac import FieldReader

        self.front.set_from_matrix(FieldReader.read_from_file())

    def wrapper_set_from_file(self, __):
        self._set_from_file()

    def _clean_up(self):
        """
        1.  Let the engine clean up
        2.  Let the field-front itself
            ->  Tk's root must also be destroyed!
        :return:
        """
        self.engine.clean_up()
        self.front.clean_up()

        # GameTk.root.destroy()

    def wrapper_clean_up(self, __):
        self._clean_up()

    @staticmethod
    def start_gui_loop() -> None:
        """
        Start Tk's (internal) main-loop.
        NOTE:
        Call this AFTER all other Tk components have been initialized:
        1.  creating key-binds.

        :return: None
        """

        GameTk.root.mainloop()


def run_entry_tk():
    GameTk((20, 10))


if __name__ == "__main__":
    run_entry_tk()
