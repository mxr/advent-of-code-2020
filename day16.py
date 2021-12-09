#!/usr/bin/env python3
import re
from argparse import ArgumentParser
from collections import defaultdict
from typing import List
from typing import NamedTuple
from typing import NewType
from typing import Tuple

RE = re.compile(r"(\d+)-(\d+)")


class Range(NamedTuple):
    min: int  # noqa: A003
    max: int  # noqa: A003

    def valid(self, n: int) -> bool:
        return self.min <= n <= self.max


class Rule(NamedTuple):
    name: str
    ranges: List[Range]

    def valid(self, n: int) -> bool:
        return any(r.valid(n) for r in self.ranges)


Ticket = NewType("Ticket", List[int])


def parse(filename: str) -> Tuple[List[Rule], Ticket, List[Ticket]]:
    with open(filename) as f:
        raw_rules, raw_yours, raw_nearby = f.read().split("\n\n")

    rules = []
    for r in raw_rules.split("\n"):
        raw_name, _, raw_ranges = r.partition(":")
        ranges = [Range(int(mn), int(mx)) for mn, mx in RE.findall(raw_ranges)]

        rules.append(Rule(raw_name.strip(), ranges))

    yours = Ticket([int(t) for t in raw_yours.splitlines()[-1].split(",")])

    nearby = [
        Ticket([int(t) for t in ticket.split(",")])
        for ticket in raw_nearby.splitlines()[1:]
    ]

    return rules, yours, nearby


def part1(filename: str) -> int:
    rules, _, nearby = parse(filename)

    return sum(
        t
        for ticket in nearby
        for t in ticket
        if not any(rule.valid(t) for rule in rules)
    )


def part2(filename: str) -> int:
    rules, yours, nearby = parse(filename)

    valid_tickets = [ticket for ticket in nearby if valid(ticket, rules)]

    names = defaultdict(set)
    for i in range(len(yours)):
        for rule in rules:
            if all(rule.valid(ticket[i]) for ticket in valid_tickets):
                names[rule.name].add(i)

    out = {}
    while names:
        positions_to_pop = []
        names_to_pop = []
        for name, positions in names.items():
            if len(positions) == 1:
                p = positions.pop()
                positions_to_pop.append(p)
                names_to_pop.append(name)
                out[name] = p

        for name, positions in names.items():
            if p in positions:
                positions.remove(p)

        for name in names_to_pop:
            del names[name]

    product = 1
    for name, position in out.items():
        if name.startswith("departure"):
            product *= yours[position]

    return product


def valid(ticket: Ticket, rules: List[Rule]) -> bool:
    return any(all(rule.valid(t) for t in ticket) for rule in rules)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("-p", "--part", type=int, default=0)
    parser.add_argument("-f", "--filename", type=str, required=True)

    args = parser.parse_args()

    part: int = args.part
    filename: str = args.filename

    if (part or 1) == 1:
        print(f"part1: {part1(filename)}")
    if (part or 2) == 2:
        print(f"part2: {part2(filename)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
