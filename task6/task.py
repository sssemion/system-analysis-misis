import json
from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass
from functools import total_ordering
from typing import Self


class FuzzySetError(Exception):
    pass


@dataclass
@total_ordering
class FuzzyElement:
    value: float
    truth: float

    def __lt__(self, other: Self | int | float) -> bool:
        if isinstance(other, (int, float)):
            return self.value < other
        return self.value < other.value

    def __eq__(self, other: Self | float) -> bool:
        if isinstance(other, (int, float)):
            return self.value == other
        return self.value == other.value


@dataclass
class Term:
    name: str
    points: list[FuzzyElement]

    def __post_init__(self) -> None:
        self.points.sort()

    def get_truth_for(self, value: float) -> float:
        idx = bisect_right(self.points, value)

        if idx == 0 or idx >= len(self.points):
            raise FuzzySetError("value вне допустимого диапазона")

        left = self.points[idx - 1]
        right = self.points[idx]

        # Линейная интерполяция
        t = left.truth + (right.truth - left.truth) * (value - left.value) / (right.value - left.value)
        return t


@dataclass
class LingVar:
    name: str
    terms: list[Term]

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        data = json.loads(json_str)
        name = list(data.keys())[0]
        terms = []
        for item in data[name]:
            terms.append(Term(item['id'], [FuzzyElement(*point) for point in item['points']]))
        return cls(name, terms)

    def fuzzify(self, value: float) -> dict[str, float]:
        return {term.name: term.get_truth_for(value) for term in self.terms}


def main(temperature_json: str, regulator_json: str, mapping_json: str, current_temperature: float) -> float:
    temperature = LingVar.from_json(temperature_json)
    regulator = LingVar.from_json(regulator_json)
    mapping = dict(json.loads(mapping_json))

    fuzzy_temperature = temperature.fuzzify(current_temperature)
    fuzzy_regulator = {mapping[item]: fuzzy_temperature[item] for item in fuzzy_temperature}

    maximums = defaultdict(list)
    for term in regulator.terms:
        t = fuzzy_regulator[term.name]
        for point in term.points:
            point.truth = min(point.truth, t)
        if t > 0:
            mx = max(term.points, key=lambda x: x.truth)
            maximums[mx.truth].append(mx.value)

    max_truth = max(maximums)
    return min(maximums[max_truth])



if __name__ == '__main__':
    args = []
    for filename in ('temperature.json', 'regulator.json', 'mapping.json'):
        with open(filename) as fd:
            args.append(fd.read())
    print(main(*args, current_temperature=19))
