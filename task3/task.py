import math

from task2.task import calc_extension_lengths, parse_tree_from_csv, RelType, INPUT_SAMPLE


def task(csv_string: str) -> float:
    root = parse_tree_from_csv(csv_string)
    ext_lengths = calc_extension_lengths(root)
    n = len(ext_lengths)
    k = len(RelType)

    entropy = 0

    for rel_type in RelType:
        for lengths in ext_lengths.values():
            l_ij = lengths[rel_type]
            if l_ij > 0:
                term = (l_ij / (n - 1)) * math.log2(l_ij / (n - 1))
                entropy += term

    entropy = -entropy
    return round(entropy, 1)


if __name__ == '__main__':
    print(task(INPUT_SAMPLE))
