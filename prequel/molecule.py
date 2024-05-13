from __future__ import annotations

from atom import Atom, ORDER, VALENCE
from errors import EmptyMolecule, UnlockedMolecule, LockedMolecule, InvalidBond


class Molecule:
    def __init__(self, name: str = "") -> None:
        self.name = name

        self.closed = False
        self.__id_tracker = 1

        self.__atoms: list[Atom] = list()
        self.__branches: list[list[Atom]] = list()

    @property
    def formula(self) -> str:
        if not self.closed:
            raise LockedMolecule('Molecule is unclosed.')

        numbers = {}
        for atom in self.__atoms:
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

        return sum(atom.weight for atom in self.__atoms)

    @property
    def atoms(self) -> list[Atom]:
        return self.__atoms.copy()
    
    def brancher(self, *args: int) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for nc in args:
            new_branch = [Atom('C', self.__id_tracker + i, []) for i in range(nc)]
            self.__id_tracker += nc

            for i in range(len(new_branch)):
                if i - 1 >= 0:
                    new_branch[i].add_neighbor(new_branch[i - 1])
                
                if i + 1 < len(new_branch):
                    new_branch[i].add_neighbor(new_branch[i + 1])

            self.__branches.append(new_branch)
            self.__atoms.extend(new_branch)
        
        return self

    def bounder(self, *args: tuple[int, int, int, int]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc1, nb1, nc2, nb2 = arg
            if nc1 == nc2 and nb1 == nb2:
                raise InvalidBond(f'Self bonding attempt at {str(self.__branches[nb1 - 1][nc1 - 1])}')
            
            first = self.__branches[nb1 - 1][nc1 - 1]
            second = self.__branches[nb2 - 1][nc2 - 1]

            if len(first.neighrs) >= first.valence or len(second.neighrs) >= second.valence:
                raise InvalidBond(f'Invalid bounder on {str(first)} with {str(second)}, atoms are full.')

            first.add_neighbor(second)
            second.add_neighbor(first)

        return self

    def mutate(self, *args: tuple[int, int, str]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb, elt = arg

            replaced = self.__branches[nb - 1][nc - 1]
            if len(replaced.neighrs) > VALENCE[elt]:
                raise InvalidBond(f'Invalid mutating {str(replaced)} to {elt}.')

            candidate = Atom(elt, replaced.id, replaced.neighrs)

            self.__branches[nb - 1][nc - 1] = candidate
            self.__atoms[self.__atoms.index(replaced)] = candidate

            for neighr in replaced.neighrs:
                neighr.mutate_neighbor(replaced.id, candidate)

        return self

    def add(self, *args: tuple[int, int, str]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb, elt = arg
            if len(self.__branches[nb - 1][nc - 1].neighrs) >= self.__branches[nb - 1][nc - 1].valence:
                raise InvalidBond(f'Invalid adding element {elt} to {str(self.__branches[nb - 1][nc - 1])}.')

            candidate = Atom(elt, self.__id_tracker, [self.__branches[nb - 1][nc - 1]])

            self.__branches[nb - 1][nc - 1].add_neighbor(candidate)
            self.__atoms.append(candidate)

            self.__id_tracker += 1
        
        return self

    def add_chaining(self, *args: tuple[int, int, list[str]]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb = arg[0], arg[1]
            if len(self.__branches[nb - 1][nc - 1].neighrs) >= self.__branches[nb - 1][nc - 1].valence:
                raise InvalidBond(f'Invalid adding chain to {str(self.__branches[nb - 1][nc - 1])}.')

            chain = [Atom(arg[i], self.__id_tracker + i, []) for i in range(2, len(arg))]
            self.__id_tracker += len(arg) - 1 # -2 + 1

            for i in range(2, len(arg)):
                if i - 1 >= 2:
                    chain[i].add_neighbor(chain[i - 1])

                if i + 1 < len(arg):
                    chain[i].add_neighbor(chain[i + 1])

            self.__branches[nb - 1][nc - 1].add_neighbor(chain[0])
            chain[0].add_neighbor(self.__branches[nb - 1][nc - 1])

        return self

    def closer(self) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is already closed.')
        
        if len(self.__branches) == 0:
            raise EmptyMolecule('Molecule is empty.')
        
        for atom in self.__atoms:
            atom.fill(self.__id_tracker)

            added = 0
            for neighr in atom.neighrs:
                if neighr.element == 'H':
                    self.__atoms.append(neighr)
                    added += 1

            self.__id_tracker += added

        self.closed = True
        return self

    def unlock(self) -> Molecule:
        if not self.closed:
            raise UnlockedMolecule('Molecule is already unlocked.')
        
        for atom in self.__atoms:
            atom.empty()
        
        self.closed = False
        return self
    
    
if __name__ == '__main__':
    pass
