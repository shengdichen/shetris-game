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


class EntryTemplate(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def init_entry(self):
        """
        Perform all startup-up work to launch the Shetris

        :return:

        """

        print("Launching Shetris")

    @abstractmethod
    def reset_entry(self):
        """
        Reset Shetris

        :return:

        """

        print("Resetting Shetris")

    @abstractmethod
    def main_loop(self):
        """
        1. PRE-phase
        2. MOVE-phase
        3. FREEZE-phase

        :return:
        """

        pass

    @abstractmethod
    def pre_phase(self):
        """
        1. generate pid
        2. generate default pos (rot is always 0)
        3. check game-over

        :return:
        """

        pass

    @abstractmethod
    def move_phase(self):
        """
        1. keep getting user's left and right
        2. receive end signal

        :return:
        """

        pass

    @abstractmethod
    def freeze_phase(self):
        """
        1. line-clear
        2. provide

        :return:
        """

        pass

    @abstractmethod
    def move_oneshot(self):
        """
        1. receive a config_delta
        2. break this down to:
            a. pre-drop rot
            b. pre-drop pos
            c. post-drop rot
            d. post-drop pos

        :return:
        """

        pass

    @abstractmethod
    def quit_entry(self):
        """
        Perform all clean-ups necessary to quit the Shetris

        :return:
        """

        print("Quitting Shetris...")


if __name__ == "__main__":
    pass
