#!/usr/bin/env python3
import math
from argparse import ArgumentParser
from typing import Dict
from typing import Generator


def parse_part1(filename: str) -> Generator[int, None, None]:
    with open(filename) as f:
        yield int(next(f))
        yield from (int(t) for t in next(f).split(",") if not t.startswith("x"))


def parse_part2(filename: str) -> Dict[int, int]:
    with open(filename) as f:
        next(f)
        return {
            i: int(t) for i, t in enumerate(next(f).split(",")) if not t.startswith("x")
        }


def part1(filename: str) -> int:
    start, *times = parse_part1(filename)

    bus_id, wait_time = min(
        ((t, t * math.ceil(start / t)) for t in times),
        key=lambda p: p[1],
    )

    return bus_id * (wait_time - start)


def part2(filename: str) -> int:
    times = parse_part2(filename)

    # https://discord.com/channels/576802746850869258/651325749638332419/792065847718838282
    step, ts = 1, 1
    for o, t in times.items():
        while (ts + o) % t:
            ts += step
        step *= t

    return ts


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
