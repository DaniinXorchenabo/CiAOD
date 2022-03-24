from os.path import join, dirname, exists
import os
from typing import Optional, IO, Generator, Iterable, Iterator, Callable
from random import randint
from math import log2
from itertools import islice
from time import process_time_ns
from abc import ABC










class Sorts(ABC):
    two_phase_sorting_by_simple_merge: Callable
    one_phase_sorting_by_simple_merge: Callable

    @classmethod
    def two_phase(cls, file_generator, file_writer, *args):
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
    def one_phase(cls, file_generator, file_writer, *args):
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
        file_generator, writer = data_
        new_cls = type(f'{cls.__name__}As{item}', (cls,), dict())
        new_cls.two_phase_sorting_by_simple_merge = staticmethod(cls.two_phase(file_generator, writer))
        new_cls.one_phase_sorting_by_simple_merge = staticmethod(cls.one_phase(file_generator, writer))

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


simple_file_generator = Sorts.get_file_gen()