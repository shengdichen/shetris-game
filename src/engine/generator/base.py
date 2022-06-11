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


class Generator(ABC):
    """
    The interface for the pid-generator

    """

    @abstractmethod
    def get_pids(self, n_pids: int = 2):
        """
        1.  Return the next n_pids of all ready pids
            ->  if (n_pids > 1) <=> (previewing enabled)

        2.  Fill in some pieces if number of ready pieces drops below the
        threshold

        :param n_pids:
        :return:
        """

        pass


if __name__ == "__main__":
    pass
