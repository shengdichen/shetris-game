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


import math

import numpy as np

from src.engine.generator.base import Generator


class _Reservoir:
    def __init__(self, refill_threshold: int):
        self._data = np.empty(0, dtype=np.uint8)
        self._refill_threshold = refill_threshold

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def refill_threshold(self):
        return self._refill_threshold

    def refill(self, new_data: np.ndarray) -> None:
        """
        Refill the reservoir by the input.

        :param new_data:
        :return:
        """

        self.data = np.append(self.data, new_data)

    def need_refill(self) -> bool:
        """
        Check if a refill is necessary

        :return:
        """

        if self.data.size < self.refill_threshold:
            return True
        else:
            return False

    def read_pop_check(self, n_items: int) -> tuple[np.ndarray, bool]:
        """
        Does exactly the name-sake:
        1.  returns the first |n_items| items of the reservoir;
        2.  pop the very first item (by definition also the first item
        returned);
        3.  runs check to signal if a refill is necessary.

        Returns a tuple of (items, need_refill)
        :param n_items:
        :return:
        """

        items = self.data[0:n_items]
        self.data = self.data[1:]
        return items, self.need_refill()


class _GeneratorBag(Generator):
    """
    Template for bag-based generator:
    Give me
    1.  a bag
    and I will give you a sequence where:
    a.  from the first generated item,
    b.  for every consecutive bag-size items,
    c.  each item of the bag appears once and once only

    Notable usages are the two sub-classes implemented below.

    """

    refill_by = 20
    refill_threshold = 10

    # this is about 15 bags
    # pre_load_amount = 100
    pre_fill = 50

    def __init__(self, bag: np.ndarray):
        self._bag = bag
        self._refill_by_bags = math.ceil(_GeneratorBag.refill_by / self.bag.size)

        self._reservoir = _Reservoir(_GeneratorBag.refill_threshold)

        # pre-fill the reservoir
        self.gen_bags(math.ceil(_GeneratorBag.pre_fill / self.bag.size))

    @property
    def bag(self):
        return self._bag

    @property
    def refill_by_bags(self):
        return self._refill_by_bags

    @property
    def reservoir(self):
        return self._reservoir

    def gen_bag(self):
        raise NotImplementedError

    def gen_bags(self, n_bags: int):
        """
        1.  Generate n_bags amount of bags;
        2.  Write the bags to the reservoir.

        Usage-cases:
        1.  When the generator is created, the reservoir is pre-filled.
        2.  Refill the reserve after amount of ready pids drops below the
        threshold after popping a pid.

        :param n_bags:
        :return:
        """

        for __ in range(n_bags):
            new_bag = self.gen_bag()
            self.reservoir.refill(new_bag)

        print("Curr ready", self.reservoir.data)

    def get_pids(self, n_pids: int = 2):
        curr_pids, need_refill = self.reservoir.read_pop_check(n_pids)

        if need_refill:
            self.gen_bags(self.refill_by_bags)

        return curr_pids


class Shuffler(_GeneratorBag):
    """
    Give me
    1.  a bag
    and I will give you
    1.  this bag, shuffled

    Init with the bag of np.arange(7) for the currently standard "7-bag"
    generator.

    """

    def __init__(self, bag: np.ndarray):
        self._rng = np.random.default_rng()
        super().__init__(bag)

    @property
    def rng(self):
        return self._rng

    def gen_bag(self) -> np.ndarray:
        return self.rng.permutation(self.bag)


class Sequencer(_GeneratorBag):
    """
    Give me:
    1.  a bag
    and I will give you:
    1.  the bag in its original order, over and over, i.e., the original bag is
    used as a fixed sequence.

    Usage:
    1.  If the bag is just one piece, we will just receive the piece over and
    over.

    """

    def __init__(self, bag: np.ndarray):
        super().__init__(bag)

    def gen_bag(self) -> np.ndarray:
        return self.bag


if __name__ == "__main__":
    pass
