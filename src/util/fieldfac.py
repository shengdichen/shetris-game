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


import os

import numpy as np


class FieldFactory:
    """
    Create the underlying (numpy) matrices of a field.

    """

    @staticmethod
    def get_all_zeros(size: tuple[int, int]) -> np.ndarray:
        """
        Produce a field of all zeros.

        :return: absolute path of this script
        """

        return np.zeros(size, dtype=bool)

    @staticmethod
    def get_all_ones(size: tuple[int, int]) -> np.ndarray:
        """
        Produce a field of all ones.

        :return: absolute path of this script
        """

        return np.ones(size, dtype=bool)


class FieldReader:
    """
    Read from file the underlying (numpy) matrices of a field.

    """

    @staticmethod
    def get_script_abs_dir() -> str:
        """
        Retrieve the absolute path of this script.

        :return: absolute path of this script
        """

        real_path = os.path.realpath(__file__)
        return os.path.dirname(real_path)

    @staticmethod
    def read_from_file(filename_rel: str = "sample") -> np.ndarray:
        """
        Read a tetris-field from a local file.

        :param filename_rel: file-name relative to the path of this script
        :return: numpy's ndarray of bool
        """

        scriptdir_abs = FieldReader.get_script_abs_dir()
        filename_abs = os.path.join(scriptdir_abs, filename_rel)

        return np.loadtxt(filename_abs, dtype=bool)


def run_reader():
    print(FieldReader.get_script_abs_dir())


def run_factory():
    print(FieldFactory.get_all_zeros((20, 10)))
    print(FieldFactory.get_all_ones((20, 10)))


if __name__ == "__main__":
    pass
