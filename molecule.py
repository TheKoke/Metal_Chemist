from __future__ import annotations
from atom import Atom
    
    
class Molecule:
    def __init__(self, name: str = '') -> None:
        self.name = name

    def brancher(self) -> Molecule:
        pass

    def bounder(self) -> Molecule:
        pass

    def mutate(self) -> Molecule:
        pass

    def add(self) -> Molecule:
        pass

    def add_chaining(self) -> Molecule:
        pass

    def close(self) -> Molecule:
        pass

    def unlock(self) -> Molecule:
        pass


if __name__ == '__main__':
    pass
