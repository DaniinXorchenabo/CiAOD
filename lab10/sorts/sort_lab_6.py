from os.path import join, dirname, exists
import os
from typing import Optional, IO, Generator, Iterable, Iterator, Callable
from random import randint
from math import log2
from itertools import islice
from time import process_time_ns
from abc import ABC

from lab10.sorts.abstract_sort import AbstractSort


class Sorts(AbstractSort):
    two_phase_sorting_by_simple_merge: Callable
    one_phase_sorting_by_simple_merge: Callable

    @classmethod
    def two_phase_6(cls, file_generator, file_writer, *args):
        def two_phase_sorting_by_simple_merge(base_file: str, part_file1: str, part_file2: str, *args,
                                              len_file: Optional[int] = None, **kwargs):
            if len_file is None:
                with open(base_file, 'r', encoding='utf-8') as base:
                    len_file = 0
                    for _ in file_generator(base):
                        len_file += 1
            time_ = process_time_ns()
            module = 2
            m = 1
            for _ in range(int(log2(len_file) + 0.5) + 1):
                with (
                        open(base_file, 'r', encoding='utf-8') as base,
                open(part_file1, 'w', encoding='utf-8') as part1,
                open(part_file2, 'w', encoding='utf-8') as part2
                ):
                    for ind, i in enumerate(file_generator(base)):
                        file_writer(i, end='', file=(part2 if ind % module >= m else part1))

                with (
                        open(part_file1, 'r', encoding='utf-8') as part1_,
                open(part_file2, 'r', encoding='utf-8') as part2_,
                open(base_file, 'w', encoding='utf-8') as base_
                ):

                    f1 = file_generator(part1_)
                    f2 = file_generator(part2_)
                    for _ in range(int(len_file / module + 0.5) + 1):
                        for i in cls.get_values(f1, f2, m):
                            file_writer(i, sep='', end='', file=base_)
                module <<= 1
                m <<= 1

            time_ = process_time_ns() - time_
            return time_

        return two_phase_sorting_by_simple_merge

    @classmethod
    def one_phase_6(cls, file_generator, file_writer, *args):
        def one_phase_sorting_by_simple_merge(base_file: str, part_file1: str, part_file2: str,
                                              part_file3: str, part_file4: str, *args,
                                              len_file: Optional[int] = None, **kwargs):
            if len_file is None:
                with open(base_file, 'r', encoding='utf-8') as base:
                    len_file = 0
                    for _ in file_generator(base):
                        len_file += 1
            time_ = process_time_ns()
            module = 2
            m = 1

            with (
                    open(base_file, 'r', encoding='utf-8') as base,
            open(part_file1, 'w', encoding='utf-8') as part1,
            open(part_file2, 'w', encoding='utf-8') as part2
            ):
                for ind, i in enumerate(file_generator(base)):
                    file_writer(i, end='', file=(part2 if ind % module >= m else part1))

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
                        for ind, i in enumerate(cls.get_values(f1, f2, m)):
                            file_writer(i, sep='', end='', file=(part3_ if _ind % 2 == 0 else part4_))

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
                for i in cls.get_values(f1, f2, len_file):
                    file_writer(i, sep='', end='', file=base_)

            time_ = process_time_ns() - time_
            return time_

        return one_phase_sorting_by_simple_merge

    def __class_getitem__(cls, data_, *item):
        print(data_, *item)
        file_generator, writer, *_ = data_
        new_cls = super().__class_getitem__( data_, *item )
        new_cls.two_phase_sorting_by_simple_merge = staticmethod(cls.two_phase_6(file_generator, writer))
        new_cls.one_phase_sorting_by_simple_merge = staticmethod(cls.one_phase_6(file_generator, writer))

        return new_cls


    @staticmethod
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
