from __future__ import annotations


class Node:
    def __init__(self, value: int, neighrs: list[Node] = []) -> None:
        self.__value = value
        self.__neighrs = neighrs

    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, new: int) -> None:
        self.__value = new

    @property
    def neighrs(self) -> list[Node]:
        return self.__neighrs[:]
    
    @property
    def degree(self) -> int:
        return len(self.__neighrs)
    
    def __eq__(self, other: Node) -> bool:
        return self.__value == other.value
    
    def add_neighbor(self, pretend: Node) -> None:
        self.__neighrs.append(pretend)


class Graph:
    def __init__(self, nodes: list[Node], adjacency: list[list[int]]) -> None:
        self.__nodes = nodes
        self.__adjacency = adjacency

    @property
    def nodes(self) -> list[Node]:
        return self.__nodes[:]
    
    @property
    def adjacency(self) -> list[list[int]]:
        return self.__adjacency.copy()
 
    def add_vertex(self, x: Node) -> None:
        new_adjacency = self.__adjacency.copy()

        for i in range(len(new_adjacency)):
            new_adjacency[i].append(0)

        new_adjacency.append([0] * len(new_adjacency) + 1)

        del self.__adjacency
        self.__adjacency = new_adjacency
        self.__nodes.append(x)

    def remove_vertex(self, x: Node) -> None:
        index = self.nodes.index(x)
        new_adjacency = self.__adjacency.copy()

        new_adjacency.pop(index)
        for i in range(len(new_adjacency)):
            new_adjacency[i].pop(index)

        del self.__adjacency
        self.__adjacency = new_adjacency
        self.__nodes.append(x)

    def add_edge(self, x: Node, y: Node, weight: int = 1) -> None:
        x_index = self.nodes.index(x)
        y_index = self.nodes.index(y)

        self.__adjacency[x_index][y_index] = weight
        self.__adjacency[y_index][x_index] = weight

    def remove_edge(self, x: Node, y: Node) -> None:
        x_index = self.nodes.index(x)
        y_index = self.nodes.index(y)

        self.__adjacency[x_index][y_index] = 0
        self.__adjacency[y_index][x_index] = 0

    @staticmethod
    def adjacent(x: Node, y: Node) -> bool:
        return x in y.neighrs and y in x.neighrs


if __name__ == '__main__':
    pass