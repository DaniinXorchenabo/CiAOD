from os.path import join, dirname
from typing import Optional, IO, Generator, Iterable, Iterator
from random import randint
from math import log2
from itertools import islice


def write_random_data_in_file(filename: str, len_: int = 100):
    with open(filename, 'w', encoding='utf-8') as base:
        for i in range(len_):
            print(chr(randint(ord('0'), ord('9'))), end='', sep='', file=base)


def file_generator(f: IO, dont_stop=False):
    char = f.read(1)
    while bool(char):
        yield char
        char = f.read(1)
    if dont_stop is True:
        while True:
            yield ""


def get_values(file1_: Generator, file2_: Generator, count: int):
    f1_ = islice(file1_, count)
    f2_ = islice(file2_, count)
    try:
        item1 = next(f1_)
    except StopIteration:
        yield from f2_
        return
    try:
        item2 = next(f2_)
    except StopIteration:
        yield item1
        yield from f1_
        return

    while True:
        if item1 < item2:
            yield item1
            try:
                item1 = next(f1_)
            except StopIteration as e:
                yield item2
                yield from f2_
                break
        else:
            yield item2
            try:
                item2 = next(f2_)
            except StopIteration as e:
                yield item1
                yield from f1_
                break


def fff1(base_file: str, part_file1: str, part_file2: str, len_file: Optional[int] = None):
    if len_file is None:
        with open(base_file, 'r', encoding='utf-8') as base:
            len_file = 0
            for _ in file_generator(base):
                len_file += 1
    module = 2
    m = 1
    for _ in range(int(log2(len_file) + 0.5)):
        print(module, m)
        with open(base_file, 'r', encoding='utf-8') as base:
            with open(part_file1, 'w', encoding='utf-8') as part1:
                with open(part_file2, 'w', encoding='utf-8') as part2:
                    for ind, i in enumerate(file_generator(base)):
                        print(i, end='', file=(part2 if ind % module >= m else part1))

        with open(part_file1, 'r', encoding='utf-8') as part1_:
            with open(part_file2, 'r', encoding='utf-8') as part2_:
                with open(base_file, 'w', encoding='utf-8') as base_:

                    f1 = file_generator(part1_)
                    f2 = file_generator(part2_)
                    for _ in range(int(len_file / module + 0.5) + 1):
                        for i in get_values(f1, f2, m):
                            print(i, sep='', end='', file=base_)
        module <<= 1
        m <<= 1


if __name__ == '__main__':

    base, f1, f2 = [join(dirname(__file__), 'files', i) for i in ['a1.txt', 'b1.txt', 'c1.txt']]
    try:
        write_random_data_in_file(base)
        fff1(base, f1, f2)
    except FileNotFoundError as e:
        for i in [base, f1, f2]:
            with open(i, 'w', encoding='utf-8') as base_:
                pass
        write_random_data_in_file(base)
        fff1(base, f1, f2)
