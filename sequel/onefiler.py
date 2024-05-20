from __future__ import annotations

class ParseHer:
    
    RADICALS    = ["meth", "eth", "prop", "but",   "pent",  "hex",  "hept",  "oct",  "non",  "dec",  "undec",  "dodec",  "tridec",  "tetradec",  "pentadec",  "hexadec",  "heptadec",  "octadec",  "nonadec"]
    MULTIPLIERS = [        "di",  "tri",  "tetra", "penta", "hexa", "hepta", "octa", "nona", "deca", "undeca", "dodeca", "trideca", "tetradeca", "pentadeca", "hexadeca", "heptadeca", "octadeca", "nonadeca"]
    
    SUFFIXES    = [         "ol",      "al", "one", "oic acid", "carboxylic acid",                "oate",               "ether", "amide", "amine", "imine", "benzene", "thiol",    "phosphine", "arsine"]
    PREFIXES    = ["cyclo", "hydroxy",       "oxo",             "carboxy",         "oxycarbonyl", "anoyloxy", "formyl", "oxy",   "amido", "amino", "imino", "phenyl",  "mercapto", "phosphino", "arsino", "fluoro", "chloro", "bromo", "iodo"]
    
    
    def __init__(self, name: str) -> None:
        pass
    
    def parse(self) -> dict[str, int]:
        pass


if __name__ == '__main__':
    pass
