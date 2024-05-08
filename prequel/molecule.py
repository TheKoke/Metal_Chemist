from __future__ import annotations

from atom import Atom, ORDER
from errors import EmptyMolecule, UnlockedMolecule, LockedMolecule, InvalidBond


class Molecule:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.closed = False

        self._branches: list[list[Atom]] = list()
        self._id_tracker = 0

    @property
    def formula(self) -> str:
        if not self.closed:
            raise LockedMolecule('Molecule is unclosed.')

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
        if not self.closed:
            raise LockedMolecule('Molecule is unclosed.')

        return sum([sum([atom.weight for atom in branch])] for branch in self._branches)

    @property
    def atoms(self) -> list[Atom]:
        all_atoms = list()
        for branch in self._branches:
            all_atoms.extend(branch)

        return all_atoms
    
    def brancher(self, *args: int) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for nc in args:
            new_branch = [Atom('C', self._id_tracker + i + 1) for i in range(nc)]
            self._id_tracker += nc

            for i in range(len(new_branch)):
                if i - 1 <= 0:
                    new_branch[i].add_neighbor(new_branch[i - 1])
                
                if i + 1 > len(new_branch):
                    new_branch[i].add_neighbor(new_branch[i + 1])

            self._branches.append(new_branch)
        
        return self

    def bounder(self, *args: tuple[int, int, int, int]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc1, nb1, nc2, nb2 = arg

            self._branches[nb1 - 1][nc1 - 1].add_neighbor(self._branches[nb2 - 1][nc2 - 1])
            self._branches[nb2 - 1][nc2 - 1].add_neighbor(self._branches[nb1 - 1][nc1 - 1])

        return self

    def mutate(self, *args: tuple[int, int, str]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb, elt = arg
            replaced = self._branches[nb - 1][nc - 1]
            candidate = Atom(elt, replaced.id, replaced.neighrs)

            self._branches[nb - 1][nc - 1] = candidate

        return self

    def add(self, *args: tuple[int, int, str]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb, elt = arg
            self._branches[nb - 1][nc - 1].add_neighbor(Atom(elt, self._id_tracker + 1, [self._branches[nb - 1][nc - 1]]))
            self._id_tracker += 1
        
        return self

    def add_chaining(self, *args: tuple[int, int, list[str]]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')

        return self

    def closer(self) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is already closed.')
        
        if len(self._branches) == 0:
            raise EmptyMolecule('Molecule is empty.')

        self.closed = True
        return self

    def unlock(self) -> Molecule:
        if not self.closed:
            raise UnlockedMolecule('Molecule is already unlocked.')
        
        self.closed = False
        return self
    
    
if __name__ == '__main__':
    pass
