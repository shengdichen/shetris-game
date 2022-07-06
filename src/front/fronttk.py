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
from tkinter import ttk

import numpy as np


class FieldTK(ttk.Frame):
    def __init__(self, tk_parent=None, size=(20, 10)):
        super().__init__(tk_parent)

        # define sizes
        self._size = size
        (
            self.outer_border_width,
            self.box_size,
            self.box_gap,
        ) = FieldTK.make_sizes()

        # colors
        (
            self.cl_background,
            self.cl_coord_0,
            self.cl_coord_1,
            self.cl_coord_active,
        ) = FieldTK.make_colors()

        self.init_frame()

        # the underlying boxes
        self._boxes = self.make_boxes()
        self.init_boxes()

        # self.set_rows(np.array([2, 3, 10]))
        # self.set_from_matrix()

    @property
    def size(self):
        return self._size

    @property
    def boxes(self):
        return self._boxes

    @staticmethod
    def make_sizes():
        """
        Define the sizes.

        :return: the sizes
        """

        outer_border_width = 20
        box_size = 40
        box_gap = 3
        return outer_border_width, box_size, box_gap

    @staticmethod
    def make_colors():
        """
        Define the fundamental colors.

        :return: the colors
        """

        cl_background = "black"
        cl_coord_0 = "grey"
        cl_coord_1 = "white"
        cl_coord_active = "white"
        return cl_background, cl_coord_0, cl_coord_1, cl_coord_active

    def init_frame(self):
        """
        1. perform stylistic setup of this ttk.Frame, which contains the field;
        2. show the frame with the grid() geometry manager.
        3. configure the grid() for displaying the boxes later.

        :return: None
        """

        # the outer border around the contents of this frame
        self["borderwidth"] = self.outer_border_width
        # (self["height"], self["width"]) = (1000, 500)

        # general style of the frame
        ttk.Style().configure("TFrame", background=self.cl_background, relief="flat")

        self.grid(row=0, column=0)

        # pre-set the sizes of all to-be-placed boxes
        (size_0, size_1) = self.size
        for row in range(size_0):
            self.grid_rowconfigure(row, minsize=self.box_size)
        for col in range(size_1):
            self.grid_columnconfigure(col, minsize=self.box_size)

    @staticmethod
    def do_for_all(f):
        """
        (Decorator)-Util to perform function f on every box.

        :param f: the function to use: must accept three arguments:
        (self, coord_0, coord_1)
        :return: None
        """

        def new_f(self):
            (range_0, range_1) = self.size

            for coord_1 in range(range_1):
                for coord_0 in range(range_0):
                    # do the actual work
                    f(self, coord_0, coord_1)

        return new_f

    def make_boxes(self):
        """
        Create all the boxes: each as a ttk.Label.

        :return:
        """

        (size_0, size_1) = self.size
        return [[ttk.Label(self) for __ in range(size_1)] for __ in range(size_0)]

    @do_for_all
    def init_boxes(self, coord_0: int, coord_1: int):
        """
        Use the do_for_all wrapper to
        1. set background of all boxes;
        2. show the boxes (with Tk's geometry-manager grid()).

        :param coord_0:
        :param coord_1:
        :return:
        """
        curr_box = self.boxes[coord_0][coord_1]
        curr_box["background"] = self.cl_coord_0

        curr_box.grid(
            row=coord_0,
            column=coord_1,
            padx=self.box_gap,
            pady=self.box_gap,
            # make sure this box really spans the whole area assigned by grid()
            sticky=tkinter.NSEW,
        )

    def set_from_matrix(self, field_matrix: np.ndarray = None):
        """
        for every 1 entries of the matrix: paint the TRUE-color

        :param field_matrix:
        :return:
        """

        self.init_boxes()

        # np.nonzero produces np's indexing; since python's raw-list is indexed
        # here, use np.argwhere
        idx_nonzero = np.argwhere(field_matrix)
        for idx_0, idx_1 in idx_nonzero:
            box_curr = self.boxes[idx_0][idx_1]
            box_curr["background"] = self.cl_coord_1

    def set_from_coords(self, coords: np.ndarray, new_color: str):
        """
        Set the boxes of some coordinates to a new-color.

        :param coords: dimension: <n_coords>x2
        :param new_color:
        :return: None
        """
        # coords = np.array(((1, 0), (2, 0), (3, 8), (7, 0)))
        for coord_0, coord_1 in coords:
            curr_box = self.boxes[coord_0][coord_1]
            curr_box["background"] = new_color

    def set_from_pair(self, coords_pair: tuple[np.ndarray, np.ndarray]):
        """
        Used after an atomic:
        1. set some old-coordinates to blank-color;
        2. set some new-coordinates to occupied-color.

        :param coords_pair: (old_coords, new_coords)
        :return: None
        """
        old_coords, new_coords = coords_pair[0], coords_pair[1]
        self.set_from_coords(old_coords, self.cl_coord_0)
        self.set_from_coords(new_coords, self.cl_coord_1)

    def clean_up(self):
        self.destroy()

    def _set_row(self, row: int, new_color: str):
        """
        Recolor one row.
        NOTE:
        1.  This is a fetcher-function for set-rows, which sets multiple rows;
            and should thus never be called directly.
        2.  This is not really expected functionality of the front-field.

        :param row:
        :param new_color:
        :return:
        """

        for box in self.boxes[row][:]:
            box["background"] = new_color

    def set_rows(self, rows: np.ndarray, new_color: str = "white"):
        """
        Recolor some rows.
        NOTE:
        1.  This is not really expected functionality of the front-field.

        :param rows:
        :param new_color:
        :return:
        """

        for row in rows:
            self._set_row(row, new_color)


def run_field_tk():
    from src.entry.tk import GameTk

    v = GameTk((20, 10))
    v.start_gui_loop()


if __name__ == "__main__":
    run_field_tk()
