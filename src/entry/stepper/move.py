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


class MovePhase:
    """
    Move-phase: from piece fully visible to end of movements

    NOTE:
    1.  the drop is NOT in move-phase:
        ->  in FREEZE-phase instead

    """

    @staticmethod
    def minimal():
        """
        1.  do nothing here
        2.  PRE-phase implicitly the only source of user input

        NOTE:
        1.  this implies absence of all tucks and spins

        :return:
        """

        return

    @staticmethod
    def atomic_only():
        """
        atomic only

        :return:
        """

        pass

    @staticmethod
    def full():
        """
        handle multis

        :return:
        """

        pass


if __name__ == "__main__":
    pass
