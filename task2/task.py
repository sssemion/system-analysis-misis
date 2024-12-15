import csv
from collections import defaultdict
from enum import Enum
from io import StringIO

from task1.task import Node, parse_tree


class RelType(Enum):
    R1 = 1  # отношение непосредственного управления (количество прямых детей),
    R2 = 2  # отношение непосредственного подчинения (1, если есть родитель, иначе 0),
    R3 = 3  # отношение опосредованного управления (количество прямых подчиненных у всех детей),
    R4 = 4  # отношение опосредованного подчинения (количество родителей на уровне выше прямого),
    R5 = 5  # отношение сопряжения на одном уровне


def main(csv_string: str) -> str:
    reader = csv.reader(csv_string.splitlines(), delimiter=',')
    edges = defaultdict[str, list](list)

    for parent, child in reader:
        edges[parent].append(child)

    root = parse_tree(dict(edges))

    extension_lengths = defaultdict[Node, dict[RelType, int]](lambda: dict.fromkeys(RelType, 0))
    level_nodes = defaultdict[int, list[Node]](list)

    def dfs(node: Node, depth: int = 0) -> None:
        extension_lengths[node][RelType.R1] = len(node.children)
        extension_lengths[node][RelType.R2] = 1 if depth > 0 else 0
        extension_lengths[node][RelType.R4] = max(0, depth - 1)
        level_nodes[depth].append(node)

        for child in node.children:
            dfs(child, depth + 1)

            extension_lengths[node][RelType.R3] += extension_lengths[child][RelType.R1]

    dfs(root)

    for depth, nodes in level_nodes.items():
        for node in nodes:
            extension_lengths[node][RelType.R5] = len(nodes) - 1

    output = StringIO()
    writer = csv.writer(output)
    for node, lengths in extension_lengths.items():
        writer.writerow(lengths.values())
    return output.getvalue()


INPUT_SAMPLE = '''
1,2
1,3
3,4
3,5
'''

if __name__ == '__main__':
    print(main(INPUT_SAMPLE.strip()))
