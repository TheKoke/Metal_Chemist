from __future__ import annotations


class Atom:
    
    def __init__ (self, elt: str, id_: int):
        self.element = elt
        self.id = id_
        
    def __hash__(self):
        return self.id
    
    def __eq__(self, other: Atom):
        return self.id == other.id
    
    def __str__(self) -> str:
        pass


if __name__ == '__main__':
    pass