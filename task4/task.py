import csv
import math


def plog(p: float) -> float:
    return -p * math.log2(p)


def main() -> list[float]:
    with open('input.csv') as fd:
        reader = csv.reader(fd)
        next(reader)  # Пропустить заголовок
        data = list(map(lambda x: list(map(int, x[1:])), reader))

    H_AB = H_A = H_B = 0.

    probabilities: list[list[float]] = [[0] * len(data[0]) for _ in range(len(data))]
    total_sum = sum(map(sum, data))
    for i in range(len(data)):
        for j in range(len(data[i])):
            p = probabilities[i][j] = data[i][j] / total_sum
            H_AB += plog(p)

        p = sum(probabilities[i])
        H_A += plog(p)

    for j in range(len(data[0])):
        p = 0
        for i in range(len(data)):
            p += probabilities[i][j]
        H_B += plog(p)

    H_a_B = 0.  # условная энтропия Ha(B)
    conditional: list[list[float]] = [[0] * len(data[0]) for _ in range(len(data))]
    for i in range(len(data)):
        denom = sum(probabilities[i])
        for j in range(len(data[i])):
            p = probabilities[i][j] / denom
            conditional[i][j] = plog(p)

    for i in range(len(conditional)):
        row = 0
        for j in range(len(conditional[i])):  # ответ по книге получается, если не умножать на log
            row += plog(conditional[i][j])
        H_a_B += row * sum(probabilities[i])

    # Количество информации I(A, B) = H(A) - Ha(B)
    I_A_B = H_A - H_a_B

    return [round(item, 2) for item in (H_AB, H_A, H_B, H_a_B, I_A_B)]


if __name__ == '__main__':
    print(main())
