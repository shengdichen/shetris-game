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


class _InputConverter:
    """
    Give me:
    1.  human's random input at terminal
    And I will:
    1.  convert this input to a tuple of integers

    """

    @staticmethod
    def _string_to_ints(move_input: str):
        """
        Common operation:
        split a string (from user's input) into many ints

        :param move_input:
        :return:
        """

        return tuple(map(int, move_input.split()))


if __name__ == "__main__":
    pass
