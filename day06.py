from collections.abc import Generator


def parse(filename: str) -> Generator[list[set[str]], None, None]:
    with open(filename) as f:
        for chunk in f.read().split("\n\n"):
            yield [set(c) for c in chunk.split()]


def part1(filename: str) -> int:
    return sum(len(answers[0].union(*answers[1:])) for answers in parse(filename))


def part2(filename: str) -> int:
    return sum(
        len(answers[0].intersection(*answers[1:])) for answers in parse(filename)
    )


if __name__ == "__main__":
    from _common import main

    raise SystemExit(main(part1, part2))
