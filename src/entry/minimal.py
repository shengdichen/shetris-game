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


from src.engine.engine import Engine
from src.entry.base import EntryTemplate
from src.entry.fetcher.human import FetcherTerminal
from src.entry.stepper.pre import PrePhase
from src.entry.stepper.freeze import FreezePhase
from src.entry.stepper.move import MovePhase


class EntryMinimal(EntryTemplate):
    """
    1.  PRE-phase
        1.  corrected
    2.  MOVE-phase:
        1.  ignored
    3.  FREEZE-phase:
        1.  include the drop

    """

    def __init__(self):
        super().__init__()

        self._engine = Engine((20, 10))

        self._fetcher = FetcherTerminal

    @property
    def engine(self):
        return self._engine

    @property
    def fetcher(self):
        return self._fetcher

    def init_entry(self):
        super().init_entry()

        self.main_loop()

    def reset_entry(self):
        super().reset_entry()

        self.engine.reset()
        self.main_loop()

    def main_loop(self):
        """
        The main-loop of the Entry-App:
        1.  repeats the life-cycle of pieces as long as game is not over
        2.  clean up when it is

        :return:
        """

        game_over = False
        while not game_over:
            if self.step():
                print("game_over")
                game_over = True

        self.reset_entry()

    def step(self):
        """
        The life-cycle of a piece
        1.  PRE-phase
            ->  if game-over: return TRUE immediately
        2.  MOVE
        3.  FREEZE-phase

        :return: TRUE is game-over; None otherwise
        """

        self.pre_phase()
        if self.engine.is_game_over:
            return True

        self.move_phase()
        self.freeze_phase()
        self.engine.field.print_field()

    def pre_phase(self):
        """
        Apply pre_phase:
        1.  use corretion
        2.  throw-away the correction-result

        :return:
        """

        def action_generator():
            return self.fetcher.pre_hinted_corrected(self.engine)

        print(self.engine.piece)
        __ = PrePhase.correction_aware(self.engine, action_generator)

    def move_phase(self):
        """
        1.  Do not allow any moving in this mode

        :return:
        """

        MovePhase.minimal()

    def freeze_phase(self):
        """
        1.  Include a drop

        :return:
        """

        FreezePhase.with_drop(self.engine)

    def quit_entry(self):
        super().quit_entry()

        self.engine.clean_up()


def run_entry():
    entry = EntryMinimal()
    entry.init_entry()


if __name__ == "__main__":
    pass
    run_entry()
