from __future__ import annotations

from atom import Atom
from branch import Brancher, BoundType
from errors import UnlockedMolecule, LockedMolecule, EmptyMolecule, InvalidBond


class Molecule:

    def __init__(self, name: str = '') -> None:
        self.name = name
        self.is_closed = False

        self.atoms: list[Atom] = list()
        self.branchers: list[Brancher] = list()

        self.__connectors = None
        self.__id_tracker = 1

    @property
    def formula(self) -> str:
        if not self.is_closed:
            raise UnlockedMolecule('To get raw formula first close molecule.')

    @property
    def molecular_weight(self) -> float:
        if not self.is_closed:
            raise UnlockedMolecule('To get molecular weight first close molecule.')

    def brancher(self, *args: list[int]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')
        
        for i in args:
            self.branchers.append(Brancher(i, self.__id_tracker))
            self.__id_tracker += i

    def __create_connectors(self) -> None:
        pass # TODO: Implement this first of all.

    def bounder(self, *args: list[tuple[int, int, int, int]]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')

    def mutate(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')

    def add(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')

    def add_chaining(self, nc: int, nb: int, *args: list[Atom]) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is locked, unlock him and try again.')

    def closer(self) -> Molecule:
        if self.is_closed:
            raise LockedMolecule('Molecule is already locked.')

    def unlock(self) -> Molecule:
        if not self.is_closed:
            raise UnlockedMolecule('Molecule is already unlocked.')


if __name__ == '__main__':
    pass
