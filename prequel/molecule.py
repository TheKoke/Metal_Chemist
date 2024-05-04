from __future__ import annotations

from atom import Atom, ORDER
from branch import Branch
from errors import EmptyMolecule, UnlockedMolecule, LockedMolecule, InvalidBond


class Molecule:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.blocked = True

        self._branches: list[Branch] = list()

    @property
    def formula(self) -> str:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')

        all_atoms = self.atoms

        numbers = {}
        for atom in all_atoms:
            if atom.element not in numbers:
                numbers[atom.element] = 1
            else:
                numbers[atom.element] += 1

        formula = ''
        for elt in ORDER:
            if elt in numbers:
                formula += elt
                if numbers[elt] > 1:
                    formula += f'{numbers[elt]}'

        return formula

    @property
    def molecular_weight(self) -> float:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')

        return sum([sum([atom.weight for atom in branch.atoms])] for branch in self._branches)

    @property
    def atoms(self) -> list[Atom]:
        all_atoms = list()
        for branch in self._branches:
            all_atoms.extend(branch.atoms)

        return all_atoms
    
    def brancher(self, *args: list[int]) -> Molecule:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')
        
        return self

    def bounder(self, *args: list[tuple[int]]) -> Molecule:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')

        return self

    def mutate(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')

        return self

    def add(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')
        
        return self

    def add_chaining(self, *args: list[tuple[int, int, str]]) -> Molecule:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')

        return self

    def closer(self) -> Molecule:
        if not self.blocked:
            raise LockedMolecule('Molecule is already locked.')
        
        if len(self._branches) == 0:
            raise EmptyMolecule('Molecule is empty.')

        self.blocked = False
        return self

    def unlock(self) -> Molecule:
        if self.blocked:
            raise UnlockedMolecule('Molecule is already unlocked.')
        
        self.blocked = True
        return self
    
    
if __name__ == '__main__':
    pass
