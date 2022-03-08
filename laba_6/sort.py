from os.path import join, dirname, exists
import os
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


def two_phase_sorting_by_simple_merge(base_file: str, part_file1: str, part_file2: str, len_file: Optional[int] = None):
    if len_file is None:
        with open(base_file, 'r', encoding='utf-8') as base:
            len_file = 0
            for _ in file_generator(base):
                len_file += 1
    module = 2
    m = 1
    for _ in range(int(log2(len_file) + 0.5)):
        with (
                open(base_file, 'r', encoding='utf-8') as base,
        open(part_file1, 'w', encoding='utf-8') as part1,
        open(part_file2, 'w', encoding='utf-8') as part2
        ):
            for ind, i in enumerate(file_generator(base)):
                print(i, end='', file=(part2 if ind % module >= m else part1))

        with (
                open(part_file1, 'r', encoding='utf-8') as part1_,
        open(part_file2, 'r', encoding='utf-8') as part2_,
        open(base_file, 'w', encoding='utf-8') as base_
        ):

            f1 = file_generator(part1_)
            f2 = file_generator(part2_)
            for _ in range(int(len_file / module + 0.5) + 1):
                for i in get_values(f1, f2, m):
                    print(i, sep='', end='', file=base_)
        module <<= 1
        m <<= 1


def one_phase_sorting_by_simple_merge(base_file: str, part_file1: str, part_file2: str,
                                      part_file3: str, part_file4: str,
                                      len_file: Optional[int] = None):
    if len_file is None:
        with open(base_file, 'r', encoding='utf-8') as base:
            len_file = 0
            for _ in file_generator(base):
                len_file += 1

    module = 2
    m = 1

    with (
            open(base_file, 'r', encoding='utf-8') as base,
            open(part_file1, 'w', encoding='utf-8') as part1,
            open(part_file2, 'w', encoding='utf-8') as part2
    ):
        for ind, i in enumerate(file_generator(base)):
            print(i, end='', file=(part2 if ind % module >= m else part1))

    for _ in range(int(log2(len_file) + 0.5)):
        with (
                open(part_file1, 'r', encoding='utf-8') as part1_,
                open(part_file2, 'r', encoding='utf-8') as part2_,
                open(part_file3, 'w', encoding='utf-8') as part3_,
                open(part_file4, 'w', encoding='utf-8') as part4_,
        ):
            f1 = file_generator(part1_)
            f2 = file_generator(part2_)
            for _ind in range(int(len_file / module + 0.5) + 1):
                for ind, i in enumerate(get_values(f1, f2, m)):
                    print(i, sep='', end='', file=(part3_ if _ind % 2 == 0 else part4_))

        m = module
        module <<= 1
        part_file1, part_file2, part_file3, part_file4 = part_file3, part_file4, part_file1, part_file2

    with (
            open(base_file, 'w', encoding='utf-8') as base_,
            open(part_file1, 'r', encoding='utf-8') as part1_,
            open(part_file2, 'r', encoding='utf-8') as part2_
    ):

        f1 = file_generator(part1_)
        f2 = file_generator(part2_)
        for i in get_values(f1, f2, len_file):
            print(i, sep='', end='', file=base_)


if __name__ == '__main__':

    base, f1_b, f1_c, f2_b, f2_c, f2_d, f2_e = [join(dirname(__file__), 'files', i) for i in
                                                ['a.txt', 'two_phase/b.txt', 'two_phase/c.txt',
                                                 'one_phase/A.txt', 'one_phase/B.txt',
                                                 'one_phase/C.txt', 'one_phase/D.txt', ]]
    len_file_ = 100
    try:

        write_random_data_in_file(base, len_file_)
        # two_phase_sorting_by_simple_merge(base, f1_b, f1_c, len_file_=len_file_)
        one_phase_sorting_by_simple_merge(base, f2_b, f2_c, f2_d, f2_e, len_file=len_file_)
    except FileNotFoundError as e:
        for i in [base, f1_b, f1_c, f2_b, f2_c, f2_d, f2_e]:
            if exists(dirname(i)) is False:
                os.makedirs(dirname(i))
            with open(i, 'w', encoding='utf-8') as base_:
                pass
        write_random_data_in_file(base, len_file_)
        # two_phase_sorting_by_simple_merge(base, f1_b, f1_c, len_file=len_file_)
        one_phase_sorting_by_simple_merge(base, f2_b, f2_c, f2_d, f2_e, len_file=len_file_)
