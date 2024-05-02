from __future__ import annotations

from atom import Atom
from errors import EmptyMolecule, UnlockedMolecule, LockedMolecule, InvalidBond


class Molecule:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.blocked = True

    @property
    def formula(self) -> str:
        pass

    @property
    def molecular_weight(self) -> float:
        pass

    @property
    def atoms(self) -> list[Atom]:
        pass
    
    def brancher(self, *args: list[int]) -> Molecule:
        return self

    def bounder(self, *args: list[tuple[int]]) -> Molecule:
        return self

    def mutate(self, *args: list[tuple[int, int, str]]) -> Molecule:
        return self

    def add(self, *args: list[tuple[int, int, str]]) -> Molecule:
        return self

    def add_chaining(self, *args: list[tuple[int, int, str]]) -> Molecule:
        return self

    def closer(self) -> Molecule:
        self.blocked = False
        return self

    def unlock(self) -> Molecule:
        self.blocked = True
        return self
    
    
if __name__ == '__main__':
    pass
