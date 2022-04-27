from __future__ import annotations
from os.path import join, dirname, exists
import os
from typing import Optional, IO, Generator, Iterable, Iterator, Callable
from random import randint, choice
from math import log2
from itertools import islice, tee
from time import process_time_ns
from abc import ABC
import enum

from lab10.sorts.abstract_sort import AbstractSort
from lab10.sorts.abstract_pre_sort import AbstractPreSort


# TypeInternalSort = AllSorts.PreInternalSort.TypeInternalSort

class Sorts(AbstractPreSort):
    internal_sorting_with_two_phase_natural_merge: Callable
    internal_sorting_with_one_phase_natural_merge: Callable

    @classmethod
    def two_phase(cls, file_generator, file_writer, pre_sorter, *args):
        def internal_sorting_with_two_phase_natural_merge(base_file: str, part_file1: str, part_file2: str, *args,
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
                    for ind, i in enumerate(pre_sorter(file_generator(base))
                                            if  count_iteration == float('inf')
                                            else file_generator(base)):
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

        return internal_sorting_with_two_phase_natural_merge

    @classmethod
    def one_phase(cls, file_generator, file_writer, pre_sorter,  *args):
        def internal_sorting_with_one_phase_natural_merge(base_file: str, part_file1: str, part_file2: str,
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
                for ind, i in enumerate(pre_sorter(file_generator(base))):
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

        return internal_sorting_with_one_phase_natural_merge

    def __class_getitem__(cls, data_, *item):
        print(data_, *item)
        sort_class_type, file_generator, writer, internal_pre_sorter, *_ = data_
        new_cls = super().__class_getitem__(data_, *item)
        new_cls.internal_sorting_with_two_phase_natural_merge = staticmethod(cls.two_phase(file_generator, writer, internal_pre_sorter))
        new_cls.internal_sorting_with_one_phase_natural_merge = staticmethod(cls.one_phase(file_generator, writer, internal_pre_sorter))

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

    class PreInternalSort(AbstractPreSort.PreInternalSort):

        @classmethod
        def get_internal_pre_sorter(cls, type_internal_sorter: TypeInternalSort, chink_size: int):
            def pre_internal_sort_decorator(func: Callable):
                nonlocal chink_size

                def new_func(file_reader: Generator, *args, **kwargs) -> Generator:
                    unsorted_array = None
                    while unsorted_array is None or len(unsorted_array) == chink_size:
                        unsorted_array = list(islice(file_reader, chink_size))
                        sorted_array: list = func(unsorted_array)
                        yield from sorted_array

                return new_func

            def dont_use_pre_sort(file_reader: Generator, *args, **kwargs):
                nonlocal chink_size
                yield from file_reader

            internal_sorters: dict[cls.TypeInternalSort, Callable] = {
                cls.TypeInternalSort.none: dont_use_pre_sort,
                cls.TypeInternalSort.quick_sort: pre_internal_sort_decorator(cls.quicksort),
            }

            return internal_sorters[type_internal_sorter]

