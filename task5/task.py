import json

import numpy as np
from numpy.typing import NDArray


def parse_matrix(clusters: list[int | list[int]]) -> NDArray:
    clusters = [c if isinstance(c, list) else [c] for c in clusters]
    n = sum(len(cluster) for cluster in clusters)

    matrix = [[1] * n for _ in range(n)]
    less = []
    for cluster in clusters:
        for worse_element in less:
            for element in cluster:
                matrix[element - 1][worse_element - 1] = 0
        for element in cluster:
            less.append(element)

    return np.array(matrix)


def main(a: str, b: str) -> str:
    matrix_a = parse_matrix(json.loads(a))
    matrix_b = parse_matrix(json.loads(b))

    matrix_and = matrix_a * matrix_b
    matrix_and_t = matrix_a.T * matrix_b.T
    matrix = np.maximum(matrix_and, matrix_and_t)

    conflict_core = set[tuple[int, int]]()
    for i in range(len(matrix)):
        for j in range(i + 1, len(matrix)):
            if matrix[i, j] == 0 and matrix[j, i] == 0:
                conflict_core.add((i + 1, j + 1))

    clusters = [pair[0] if len(pair) == 1 else pair for pair in sorted(conflict_core)]
    return json.dumps(clusters)


A = '[1,[2,3],4,[5,6,7],8,9,10]'
B = '[[1,2],[3,4,5],6,7,9,[8,10]]'

if __name__ == '__main__':
    print(main(A, B))
