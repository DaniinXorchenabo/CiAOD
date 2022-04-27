from os.path import join, dirname, exists
import os
from typing import Optional, IO, Generator, Iterable, Iterator, Callable
from random import randint
from math import log2
from itertools import islice, tee
from time import process_time_ns
from abc import ABC

from lab10.sorts.abstract_sort import AbstractSort


class Sorts(AbstractSort):
    two_phase_sorting_by_natural_merge: Callable
    one_phase_sorting_by_natural_merge: Callable

    @classmethod
    def two_phase_7(cls, file_generator, file_writer, *args):
        def two_phase_sorting_by_natural_merge(base_file: str, part_file1: str, part_file2: str, *args,
                                              len_file: Optional[int] = None, **kwargs):
            if len_file is None:
                with open(base_file, 'r', encoding='utf-8') as base:
                    len_file = 0
                    for _ in file_generator(base):
                        len_file += 1
            time_ = process_time_ns()
            count_iteration = float('inf')
            while count_iteration > 1:
                with (
                        open(base_file, 'r', encoding='utf-8') as base,
                open(part_file1, 'w', encoding='utf-8') as part1,
                open(part_file2, 'w', encoding='utf-8') as part2
                ):
                    last_i = chr(0)
                    counter_ = 0
                    for ind, i in enumerate(file_generator(base)):
                        if last_i > i:
                            counter_ += 1
                        file_writer(i, end='', file=(part2 if counter_ % 2 == 1 else part1))
                        last_i = i

                        # print("-=-=", ind)

                with (
                        open(part_file1, 'r', encoding='utf-8') as part1_,
                open(part_file2, 'r', encoding='utf-8') as part2_,
                open(base_file, 'w', encoding='utf-8') as base_
                ):

                    f1 = file_generator(part1_)
                    f2 = file_generator(part2_)
                    count_iteration = 0
                    for gen in cls.get_values(f1, f2):
                        count_iteration += 1
                        for i in gen:
                            file_writer(i, sep='', end='', file=base_)
                            # print('**===', i)
                        # print(count_iteration)

            time_ = process_time_ns() - time_
            return time_

        return two_phase_sorting_by_natural_merge

    @classmethod
    def one_phase_7(cls, file_generator, file_writer, *args):
        def one_phase_sorting_by_natural_merge(base_file: str, part_file1: str, part_file2: str,
                                              part_file3: str, part_file4: str, *args,
                                              len_file: Optional[int] = None, **kwargs):
            if len_file is None:
                with open(base_file, 'r', encoding='utf-8') as base:
                    len_file = 0
                    for _ in file_generator(base):
                        len_file += 1
            time_ = process_time_ns()

            with (
                    open(base_file, 'r', encoding='utf-8') as base,
            open(part_file1, 'w', encoding='utf-8') as part1,
            open(part_file2, 'w', encoding='utf-8') as part2
            ):
                last_i = chr(0)
                counter_ = 0
                for ind, i in enumerate(file_generator(base)):
                    if last_i > i:
                        counter_ += 1
                    file_writer(i, end='', file=(part2 if counter_ % 2 == 1 else part1))
                    last_i = i

            count_iteration = float('inf')
            # print('________0000000')
            while count_iteration > 1:
                with (
                        open(part_file1, 'r', encoding='utf-8') as part1_,
                open(part_file2, 'r', encoding='utf-8') as part2_,
                open(part_file3, 'w', encoding='utf-8') as part3_,
                open(part_file4, 'w', encoding='utf-8') as part4_,
                ):

                    f1 = file_generator(part1_)
                    f2 = file_generator(part2_)
                    count_iteration = 0
                    for _ind, gen in enumerate(cls.get_values(f1, f2)):
                        count_iteration += 1
                        for i in gen:
                            file_writer(i, sep='', end='', file=(part3_ if _ind % 2 == 0 else part4_))
                            # print('**===', i)
                        # print(count_iteration)

                part_file1, part_file2, part_file3, part_file4 = part_file3, part_file4, part_file1, part_file2

            with (
                    open(base_file, 'w', encoding='utf-8') as base_,
            open(part_file1, 'r', encoding='utf-8') as part1_,
            open(part_file2, 'r', encoding='utf-8') as part2_
            ):

                f1 = file_generator(part1_)
                f2 = file_generator(part2_)
                count_iteration = 0
                for _ind, gen in enumerate(cls.get_values(f1, f2)):
                    count_iteration += 1
                    for i in gen:
                        file_writer(i, sep='', end='', file=base_)

            time_ = process_time_ns() - time_
            return time_

        return one_phase_sorting_by_natural_merge

    def __class_getitem__(cls, data_, *item):
        print(data_, *item)
        file_generator, writer, *_ = data_
        new_cls = super().__class_getitem__(data_, *item)
        new_cls.two_phase_sorting_by_natural_merge = staticmethod(cls.two_phase_7(file_generator, writer))
        new_cls.one_phase_sorting_by_natural_merge = staticmethod(cls.one_phase_7(file_generator, writer))

        return new_cls

    @staticmethod
    def get_values(file1_: Generator, file2_: Generator):

        def crop_file_gen(f: Generator):
            try:
                item = next(f)
            except StopIteration:
                yield iter([])
                return

            def _crop_file_gen(f: Generator):
                nonlocal item
                # last_item = float('-inf')
                while item != -1:
                    try:
                        yield item
                        last_item = item
                        item = next(f)
                    except StopIteration as e:
                        # raise StopIteration() from e
                        item = -1
                        return
                        # yield item
                        # break
                    if last_item > item:
                        break

            res = _crop_file_gen(f)
            while item != -1:
                yield res
                res = _crop_file_gen(f)


        generator_of_file_generators_1 = crop_file_gen(file1_)
        generator_of_file_generators_2 = crop_file_gen(file2_)

        def merge_files(f1_, f2_):
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
                # print(item1, item2)
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

        while True:
            try:
                f1_gen = next(generator_of_file_generators_1)
            except StopIteration:
                for gen in generator_of_file_generators_2:
                    yield gen
                break
            try:
                f2_gen = next(generator_of_file_generators_2)
            except StopIteration:
                yield f1_gen
                for gen in generator_of_file_generators_1:
                    yield gen
                break

            yield merge_files(f1_gen, f2_gen)

