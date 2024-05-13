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

ORDER = {
    'C' : 1,
    'H' : 2,
    'O' : 3, 
    'B' : 4,
    'Br': 5,
    'Cl': 6,
    'F' : 7,
    'Mg': 8,
    'N' : 9,
    'P' : 10,
    'S' : 11
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
        neighrs_queue = sorted(self.__neighrs, key=lambda x: ORDER[x.element] * 10 + x.id)

        neighrs = []
        for atom in neighrs_queue:
            if atom.element == 'H': 
                continue

            neighrs.append(f'{atom.element}{atom.id}')

        for atom in neighrs_queue:
            if atom.element == 'H':
                neighrs.append(f'{atom.element}')
        
        if len(neighrs) > 0:
            string += ': '
            string += ','.join(neighrs)

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
    
    def mutate_neighbor(self, origin_id: int, mutating: Atom) -> bool:
        try:
            replaced_index = next(i for i in range(len(self.__neighrs)) if self.__neighrs[i].id == origin_id)
        except:
            return False

        self.__neighrs[replaced_index] = mutating
        return True
    
    def fill(self, id: int) -> None:
        while len(self.neighrs) < self.valence:
            self.add_neighbor(Atom('H', id, [self]))
            id += 1

    def empty(self) -> None:
        while any([atom for atom in self.__neighrs if atom.element == 'H']):
            found = next(i for i in range(len(self.__neighrs)) if self.__neighrs[i].element == 'H')
            self.neighrs.pop(found)


if __name__ == '__main__':
    pass
