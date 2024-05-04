from __future__ import annotations

from atom import Atom


class Branch:
    def __init__(self, nc: int, id_start: int = 0) -> None:
        self.atoms = [Atom('C', id_start + i + 1) for i in range(nc)]
        self.adj = Branch.__create_adjacency(self.atoms)

    @staticmethod
    def __create_adjacency(carbons: list[Atom]) -> list[list[int]]:
        # C-C-C-C-...-C
        adj = [[0] * len(carbons)] * len(carbons)

        for i in range(len(carbons) - 1):
            adj[i][i + 1] = 1
            adj[i + 1][i] = 1

        return adj
    
    def mutate(self, nc: int, elt: str) -> None:
        pass
    
    def add(self, nc: int, elt: str) -> None:
        pass

    def add_chaining(self, nc: int, *args: list[str]) -> None:
        pass

    def add_bound(self, x: Atom, y: Atom, bounds: int = 1) -> None:
        x_index = self.atoms.index(x)
        y_index = self.atoms.index(y)

        self.adj[x_index][y_index] = bounds
        self.adj[y_index][x_index] = bounds

    @staticmethod
    def adjacent(x: Atom, y: Atom) -> bool:
        return x in y.neighrs and y in x.neighrs


if __name__ == '__main__':
    pass
