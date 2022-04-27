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


# from random


class Sorts(ABC):
    two_phase_sorting_by_simple_merge: Callable
    one_phase_sorting_by_simple_merge: Callable

    @classmethod
    def two_phase(cls, file_generator, file_writer, pre_sorter, *args):
        def two_phase_sorting_by_simple_merge(base_file: str, part_file1: str, part_file2: str, *args,
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

        return two_phase_sorting_by_simple_merge

    @classmethod
    def one_phase(cls, file_generator, file_writer, pre_sorter,  *args):
        def one_phase_sorting_by_simple_merge(base_file: str, part_file1: str, part_file2: str,
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

        return one_phase_sorting_by_simple_merge

    def __class_getitem__(cls, data_, *item):
        print(data_, *item)
        file_generator, writer, internal_pre_sorter = data_
        new_cls = type(f'{cls.__name__}As{item}', (cls,), dict())
        new_cls.two_phase_sorting_by_simple_merge = staticmethod(cls.two_phase(file_generator, writer, internal_pre_sorter))
        new_cls.one_phase_sorting_by_simple_merge = staticmethod(cls.one_phase(file_generator, writer, internal_pre_sorter))

        return new_cls

    @staticmethod
    def write_random_data_in_file(filename: str, len_: int = 100, data_: Optional[str] = None):
        with open(filename, 'w', encoding='utf-8') as base:
            if data_ is None:
                data_: str = ''.join([chr(randint(ord('0'), ord('9'))) for i in range(len_)])
                print(data_, end='', sep='', file=base)
            else:
                print(data_, end='', sep='', file=base)
        return data_

    @staticmethod
    def get_file_gen(get_history: bool = False, count_of_read: bool = False):
        static_variables = {'count_of_read': 0, "history": dict()}

        if get_history is True and count_of_read is True:

            def count_read_file_generator(f: IO, dont_stop=False,
                                          __static_variables=static_variables,
                                          return_static_variables: bool = False):
                if return_static_variables is True:
                    yield __static_variables
                    return __static_variables
                char = f.read(1)
                if bool(char):
                    static_variables["count_of_read"] += 1
                    static_variables["history"][f] = static_variables["history"].get(f, "") + char
                while bool(char):
                    yield char
                    char = f.read(1)
                    if bool(char):
                        static_variables["count_of_read"] += 1
                        static_variables["history"][f] = static_variables["history"].get(f, "") + char
                if dont_stop is True:
                    while True:
                        yield ""
                return


        elif get_history is True:
            static_variables['count_of_read'] = "?"

            def count_read_file_generator(f: IO, dont_stop=False,
                                          __static_variables=static_variables,
                                          return_static_variables: bool = False):
                if return_static_variables is True:
                    yield __static_variables
                    return __static_variables
                char = f.read(1)
                if bool(char):
                    static_variables["history"][f] = static_variables["history"].get(f, "") + char
                while bool(char):
                    yield char
                    char = f.read(1)
                    if bool(char):
                        static_variables["history"][f] = static_variables["history"].get(f, "") + char
                if dont_stop is True:
                    while True:
                        yield ""
                return

        elif count_of_read is True:
            static_variables['history'] = ""

            def count_read_file_generator(f: IO, dont_stop=False,
                                          __static_variables=static_variables,
                                          return_static_variables: bool = False):
                if return_static_variables is True:
                    yield __static_variables
                    return __static_variables
                char = f.read(1)
                if bool(char):
                    static_variables["count_of_read"] += 1
                while bool(char):
                    yield char
                    char = f.read(1)
                    if bool(char):
                        static_variables["count_of_read"] += 1
                if dont_stop is True:
                    while True:
                        yield ""
                return

        else:
            static_variables['count_of_read'] = "?"
            static_variables['history'] = ""

            def count_read_file_generator(f: IO, dont_stop=False,
                                          __static_variables=static_variables,
                                          return_static_variables: bool = False
                                          ):
                if return_static_variables is True:
                    yield __static_variables
                    return __static_variables
                char = f.read(1)
                while bool(char):
                    yield char
                    char = f.read(1)
                if dont_stop is True:
                    while True:
                        yield ""
                return

        return count_read_file_generator

    @staticmethod
    def get_write_file_func(count_of_write: bool = False):
        static_variables = {'count_of_write': 0}

        if count_of_write is True:

            def write_file(*string: str, file: IO = None, sep: str = '', end: str = '',
                           __static_variables=static_variables,
                           return_static_variables: bool = False):
                if return_static_variables is True:
                    return __static_variables
                assert file is not None
                print(*string, sep=sep, end=end, file=file)
                __static_variables['count_of_write'] += sum([len(i) for i in string])

        else:
            static_variables['count_of_write'] = '?'

            def write_file(*string: str, file: IO = None, sep: str = '', end: str = '',
                           __static_variables=static_variables,
                           return_static_variables: bool = False):
                if return_static_variables is True:
                    return __static_variables
                assert file is not None
                print(*string, sep=sep, end=end, file=file)

        return write_file

    @staticmethod
    def old_get_values(file1_: Generator, file2_: Generator, count: int):
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

    class PreInternalSort(object):

        class TypeInternalSort(str, enum.Enum):
            quick_sort = "quick_sort"
            none = "none"

        @classmethod
        def get_internal_pre_sorter(cls, type_internal_sorter: TypeInternalSort, chink_size: int):

            def dont_use_pre_sort(file_reader: Generator, *args, **kwargs):
                nonlocal chink_size
                yield from file_reader

            def pre_internal_sort_decorator(func: Callable):
                nonlocal chink_size
                def new_func(file_reader: Generator, *args, **kwargs) -> Generator:
                    unsorted_array = None
                    while  unsorted_array is None or len(unsorted_array) == chink_size:
                        unsorted_array = list(islice(file_reader, chink_size))
                        sorted_array: list = func(unsorted_array)
                        yield from sorted_array

                return new_func

            @pre_internal_sort_decorator
            def quicksort(a: list):
                def _quicksort(nums):
                    if len(nums) <= 1:
                        return nums
                    else:
                        q = choice(nums)
                    l_nums = [n for n in nums if n < q]

                    e_nums = [q] * nums.count(q)
                    b_nums = [n for n in nums if n > q]
                    return _quicksort(l_nums) + e_nums + _quicksort(b_nums)

                return _quicksort(a)

            internal_sorters: dict[cls.TypeInternalSort, Callable] = {
                cls.TypeInternalSort.none: dont_use_pre_sort,
                cls.TypeInternalSort.quick_sort: quicksort,
            }

            return internal_sorters[type_internal_sorter]




simple_file_generator = Sorts.get_file_gen()
