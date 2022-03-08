from os.path import join, dirname
from typing import Optional, IO, Generator, Iterable, Iterator
from random import randint
from math import log2
from itertools import islice

# import python_sql_mixins

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
    f1_: Iterable = islice(file1_, count)  # zip(file1_, range(count))
    f2_: Iterable  = islice(file2_, count)  # zip(file2_, range(count))
    try:
        item1 = next(f1_)
    except StopIteration as e:
        yield from f2_
        return
    try:
        item2 = next(f2_)
    except StopIteration as e:
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




# def fff(base_file: str, part_file1: str, part_file2: str, len_file: Optional[int] = None):
#     if len_file is None:
#         with open(base_file, 'r', encoding='utf-8') as base:
#             # base.
#             len_file = 0
#             for _ in file_generator(base):
#                 len_file += 1
#                 # print(_)
#     module = 2
#     m = 1
#     for _ in range(int(log2(len_file) + 0.5)):
#         with (
#                 open(base_file, 'r', encoding='utf-8') as base,
#                 open(part_file1, 'w', encoding='utf-8') as part1,
#                 open(part_file2, 'w', encoding='utf-8') as part2
#         ):
#
#             for ind, i in enumerate(file_generator(base)):
#                 print(i, end='', file=(part2 if ind % module >= m else part1))
#             module <<= 2
#             m <<= 1
#
#         with (
#                 open(base_file, 'w', encoding='utf-8') as base,
#                 open(part_file1, 'r', encoding='utf-8') as part1,
#                 open(part_file2, 'r', encoding='utf-8') as part2
#         ):
#             f1 = file_generator(part1)
#             f2 = file_generator(part2)
#             item1 = next(f1)
#             item2 = next(f2)
#             current_item = item1
#             current_gen = f1
#             for ind in range(len_file + 1):
#                 if item1 < item2:
#                     print(item1, end='', file=base)
#                     try:
#                         item1 = next(f1)
#                     except StopIteration as e:
#                         current_item = item2
#                         current_gen = f2
#                         break
#                 else:
#                     print(item2, end='', file=base)
#                     try:
#                         item2 = next(f2)
#                     except StopIteration as e:
#                         current_item = item1
#                         current_gen = f1
#                         break
#             print(current_item, end='', file=base)
#             for char in current_gen:
#                 print(char, end='', file=base)
#             print('')
#         # with (
#         #         open(base_file, 'r', encoding='utf-8') as base):
#         #     print(len([i for i in base.read()]))

def fff1(base_file: str, part_file1: str, part_file2: str, len_file: Optional[int] = None):
    if len_file is None:
        with open(base_file, 'r', encoding='utf-8') as base:
            # base.
            len_file = 0
            for _ in file_generator(base):
                len_file += 1
                # print(_)
    module = 2
    m = 1
    for _ in range(int(log2(len_file) + 0.5)):
        print(module, m)
        with open(base_file, 'r', encoding='utf-8') as base:
            with open(part_file1, 'w', encoding='utf-8') as part1:
                with open(part_file2, 'w', encoding='utf-8') as part2:
                    for ind, i in enumerate(file_generator(base)):
                        print(i, end='', file=(part2 if ind % module >= m else part1))
                        # print(str(ind).center(3) + ' % ' + str(module).center(4) + ' >= ' + str(m).center(4) + 'is:', ind % module >= m)


        with open(part_file1, 'r', encoding='utf-8') as part1_:
            with open(part_file2, 'r', encoding='utf-8') as part2_:
                with open(base_file, 'w', encoding='utf-8') as base_:

                    f1 = file_generator(part1_)
                    f2 = file_generator(part2_)
                    for _ in range(int(len_file / module + 0.5) + 1):
                        for i in get_values(f1, f2, m):
                            print(i, sep='', end='', file=base_)
                            print(i, sep='', end='')
        module <<= 1
        m <<= 1
        print()


if __name__ == '__main__':
    from python_sql_mixins import python_sql_mixins
    # python_sql_mixins.test()
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

