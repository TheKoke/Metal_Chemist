from __future__ import annotations

from atom import Atom, ORDER
from branch import Brancher, BoundType, Connector
from errors import UnlockedMolecule, LockedMolecule, EmptyMolecule, InvalidBond


class Molecule:

    def __init__(self, name: str = '') -> None:
        self.name = name
        self.is_closed = False

        self.atoms: list[Atom] = list()
        self.branchers: list[Brancher] = list()

        self.connectors: list[Connector] = None
        self.__id_tracker = 1

    @property
    def formula(self) -> str:
        if not self.is_closed:
            raise UnlockedMolecule('To get raw formula first close molecule.')
        
        mapper = dict()
        for atom in self.atoms:
            if atom.element in mapper.keys():
                mapper[atom.element] += 1
            else:
                mapper[atom.element] = 1

        string = ''
        for elt in ORDER:
            if elt in mapper.keys():
                string += f'{elt}{mapper[elt]}' if mapper[elt] > 1 else f'{elt}'

        return string

    @property
    def molecular_weight(self) -> float:
        if not self.is_closed:
            raise UnlockedMolecule('To get molecular weight first close molecule.')
        
        return sum([atom.weight for atom in self.atoms])

    def brancher(self, *args: list[int]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')
        
        for i in args:
            self.branchers.append(Brancher(i, self.__id_tracker))
            self.__id_tracker += i

        self.__create_connectors()
        return self

    def __create_connectors(self) -> None:
        self.connectors = []
        for i in range(len(self.branchers) - 1):
            for j in range(i, len(self.branchers)):
                pass

    def bounder(self, *args: list[tuple[int, int, int, int]]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')
        
        return self

    def mutate(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')
        
        for arg in args:
            self.branchers[arg[1]].mutate(arg[0], arg[2])

        return self

    def add(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')
        
        for arg in args:
            current = Atom(arg[2], self.__id_tracker)
            self.__id_tracker += 1

            self.branchers[arg[1]].atoms[arg[0]].add_neighbor(current)

        return self

    def add_chaining(self, nc: int, nb: int, *args: list[str]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')
        
        chaining = [Atom(args[i], self.__id_tracker + i) for i in range(len(args))]
        self.__id_tracker += len(args)

        for i in range(len(chaining)):
            chaining[i - 1].add_neighbor(chaining[i])
            chaining[i].add_neighbor(chaining[i - 1])

        self.branchers[nb - 1].atoms[nc - 1].add_neighbor(chaining[0])
        return self

    def closer(self) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is already locked.')
        
        for branch in self.branchers:
            branch.lock()
        
        self.is_closed = True
        return self

    def unlock(self) -> Molecule:
        if not self.is_closed:
            raise UnlockedMolecule('Molecule is already unlocked.')
        
        for branch in self.branchers:
            branch.unlock()
        
        self.is_closed = True
        return self


if __name__ == '__main__':
    pass
