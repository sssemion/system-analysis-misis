from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any


class InvalidTree(Exception):
    pass


@dataclass
class Node:
    value: Any
    children: list[Node] = field(default_factory=list)

    def __hash__(self):
        return hash(self.value)

def print_tree(node: Node, _indent: int = 0) -> None:
    print('\t' * _indent, node.value)
    for ch in node.children:
        print_tree(ch, _indent + 1)


def main(path: str) -> Node:
    with open(path) as fd:
        nodes = json.load(fd)['nodes']

    cache = dict[str, Node]()
    root_cache = dict[Node, bool]()
    for k, children in nodes.items():
        if (node := cache.get(k)) is None:
            node = cache[k] = Node(k)
            root_cache.setdefault(node, True)

        for ch in children:
            if (ch_node := cache.get(ch)) is None:
                ch_node = cache[ch] = Node(ch)
            node.children.append(ch_node)
            root_cache[ch_node] = False

    roots = [node for node, is_root in root_cache.items() if is_root]
    if len(roots) > 1:
        raise InvalidTree('Более одного корня')
    elif not roots:
        raise InvalidTree('Цикличное дерево')

    root = roots[0]
    print_tree(root)
    return root


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    main(args.filename)


if __name__ == '__main__':
    cli()
