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


class CommonUtil:
    @staticmethod
    def get_script_abs_dir() -> str:
        """
        Retrieve the absolute path of this script.

        :return: absolute path of this script
        """

        real_path = os.path.realpath(__file__)
        return os.path.dirname(real_path)

    @staticmethod
    def get_filename_abs(filename_rel: str):
        """
        Retrieve the absolute filename from filename relative to script-dir

        :param filename_rel:
        :return:
        """

        scriptdir_abs = CommonUtil.get_script_abs_dir()
        filename_abs = os.path.join(scriptdir_abs, filename_rel)

        return filename_abs


def abs_dir_test():
    print(CommonUtil.get_script_abs_dir())
    print(CommonUtil.get_filename_abs("test_name"))


if __name__ == "__main__":
    pass
