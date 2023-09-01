from __future__ import annotations

from enum import Enum

from atom import Atom
from errors import *


class BoundType(Enum):
    NONE = 0
    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3


class Brancher:

    def __init__(self, carbons: int, id_start: int) -> None:
        self.atoms = [Atom('C', i) for i in range(id_start, id_start + carbons)]
        self.adjacency = self.__create_adjacency_matrix()

    def __create_adjacency_matrix(self) -> list[list[BoundType]]:
        adj = [[BoundType.NONE * len(self.atoms)] * len(self.atoms)]

        for i in range(1, len(self.atoms)):
            self.atoms[i - 1].add_neighbor(self.atoms[i])
            self.atoms[i].add_neighbor(self.atoms[i - 1])

            adj[i - 1][i] = BoundType.SINGLE
            adj[i][i - 1] = BoundType.SINGLE

        return adj

    def mutate(self) -> None:
        pass


if __name__ == '__main__':
    pass
