from __future__ import annotations
from enum import Enum


VALENCE = { 'H' : 1, 'B' : 3, 'C' : 4, 'N' : 3, 'O' : 2, 'F' : 1, 'Mg': 2, 'P' : 3, 'S' : 2, 'Cl': 1, 'Br': 1 }
WEIGHT = { 'H' :  1.0, 'B' : 10.8, 'C' : 12.0, 'N' : 14.0, 'O' : 16.0, 'F' : 19.0, 'Mg': 24.3, 'P' : 31.0, 'S' : 32.1, 'Cl': 35.5, 'Br': 80.0 }
ORDER = { 'C' : 1, 'H' : 2, 'O' : 3,  'B' : 4, 'Br': 5, 'Cl': 6, 'F' : 7, 'Mg': 8, 'N' : 9, 'P' : 10, 'S' : 11 }


class EmptyMolecule(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnlockedMolecule(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LockedMolecule(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidBond(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Atom:
    
    def __init__ (self, elt: str, id: int, neighrs: list[Atom] = []):
        self.__element = elt
        self.__id = id

        self.__neighrs = neighrs
        
    def __hash__(self):
        return self.id
    
    def __eq__(self, other: Atom):
        return self.id == other.id
    
    def __str__(self) -> str:
        string = f'Atom({self.__element}.{self.__id}: '
        neighrs_queue = sorted(self.__neighrs, key=lambda x: ORDER[x.element] * 100 + x.id)

        neighrs = []
        for atom in neighrs_queue:
            if atom.element == 'H':
                neighrs.append(f'{atom.element}')
                continue

            neighrs.append(f'{atom.element}{atom.id}')

        string += ','.join(neighrs) if len(neighrs) > 0 else ''

        string += ')'
        return string

    @property
    def element(self) -> str:
        return self.__element
    
    @property
    def valence(self) -> int:
        return VALENCE[self.__element]
    
    @property
    def weight(self) -> float:
        return WEIGHT[self.__element]
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def neighrs(self) -> list[Atom]:
        return self.__neighrs.copy()
    
    def add_neighbor(self, atom: Atom) -> bool:
        if self.valence <= len(self.neighrs):
            return False
        
        self.__neighrs.append(atom)
        return True
    
    def fill(self, id: int) -> None:
        while len(self.neighrs) < self.valence:
            self.add_neighbor(Atom('H', id, [self]))
            id += 1

    def empty(self) -> None:
        while any([atom for atom in self.__neighrs if atom.element == 'H']):
            found = next(i for i in range(len(self.__neighrs)) if self.__neighrs[i].element == 'H')
            self.neighrs.pop(found)


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

            self.__branches[nb1 - 1][nc1 - 1].add_neighbor(self.__branches[nb2 - 1][nc2 - 1])
            self.__branches[nb2 - 1][nc2 - 1].add_neighbor(self.__branches[nb1 - 1][nc1 - 1])

        return self

    def mutate(self, *args: tuple[int, int, str]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb, elt = arg

            replaced = self.__branches[nb - 1][nc - 1]
            candidate = Atom(elt, replaced.id, replaced.neighrs)

            self.__branches[nb - 1][nc - 1] = candidate
            self.__atoms[self.__atoms.index(replaced)] = candidate

        return self

    def add(self, *args: tuple[int, int, str]) -> Molecule:
        if self.closed:
            raise LockedMolecule('Molecule is closed.')
        
        for arg in args:
            nc, nb, elt = arg

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
