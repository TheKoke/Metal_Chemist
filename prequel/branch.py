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
    
    def add_atom(self, x: Atom) -> None:
        new_adjacency = self.adj.copy()

        for i in range(len(new_adjacency)):
            new_adjacency[i].append(0)

        new_adjacency.append([0] * len(new_adjacency) + 1)

        del self.adj
        self.adj = new_adjacency
        self.atoms.append(x)

    def remove_atom(self, x: Atom) -> None:
        index = self.atoms.index(x)
        new_adjacency = self.adj.copy()

        new_adjacency.pop(index)
        for i in range(len(new_adjacency)):
            new_adjacency[i].pop(index)

        del self.adj
        self.adj = new_adjacency
        self.atoms.append(x)

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
