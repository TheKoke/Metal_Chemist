

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


if __name__ == '__main__':
    pass
