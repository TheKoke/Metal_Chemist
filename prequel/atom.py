from __future__ import annotations


VALENCE = {
    'H' : 1,
    'B' : 3,
    'C' : 4,
    'N' : 3,
    'O' : 2,
    'F' : 1,
    'Mg': 2,
    'P' : 3,
    'S' : 2,
    'Cl': 1,
    'Br': 1
}

WEIGHT = {
    'H' :  1.0,
    'B' : 10.8,
    'C' : 12.0,
    'N' : 14.0,
    'O' : 16.0,
    'F' : 19.0,
    'Mg': 24.3,
    'P' : 31.0,
    'S' : 32.1,
    'Cl': 35.5,
    'Br': 80.0
}


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
        string = f'Atom({self.__element}.{self.__id}'

        neighrs = []
        for atom in set(self.__neighrs):
            if atom.element == 'H':
                neighrs.append(f'{atom.element}')

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
        return self.__neighrs[:]
    
    def add_neighbor(self, atom: Atom) -> bool:
        if self.valence <= len(self.neighrs):
            return False
        
        self.__neighrs.append(atom)
        return True


if __name__ == '__main__':
    pass
