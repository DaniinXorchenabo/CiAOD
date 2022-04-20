from __future__ import annotations
from os.path import join, dirname, exists
import os
from typing import Optional, IO, Generator, Iterable, Iterator, Callable, Type
from random import randint, choice
from math import log2
from itertools import islice, tee
from time import process_time_ns
from abc import ABC
import enum
from file_iter_controller import FileIteratorAbstract


# from random


class Sorts(ABC):
    selection_sort: Callable

    @classmethod
    def selection_sort_producer(cls, file_control_class: Type[FileIteratorAbstract], pre_sorter, *args):

        def selection_sort_(base_file: str, *args, len_file: Optional[int] = None, **kwargs):
            chink_size = 3
            if len_file is None:
                with open(base_file, 'rb', encoding='utf-8') as base:
                    len_file = len(base.read())

            time_ = process_time_ns()
            count_iteration = float('inf')

            begin_current_fragment = len_file
            begin_last_fragment = len_file
            with open(base_file, 'rb+') as base:

                file_controller = file_control_class(base)
                file_controller.move_to_tail()

                begin_last_fragment = begin_current_fragment
                begin_current_fragment -= chink_size
                file_controller.pointer_move_absolute(begin_current_fragment)
                file_controller.print_file()

                unsorted_data: str = file_controller.read(chink_size)
                file_controller.print_file()
                sorted_data = list(pre_sorter(unsorted_data))
                file_controller.pointer_move_relative(-chink_size)
                file_controller.print_file()
                file_controller.write(sorted_data)
                file_controller.print_file()
                print('='*10)
                while begin_current_fragment > 0:

                    begin_last_fragment = begin_current_fragment
                    begin_current_fragment -= chink_size
                    _begin_current_fragment = begin_current_fragment
                    begin_current_fragment = max(0, begin_current_fragment)
                    chink_size = chink_size + (_begin_current_fragment - begin_current_fragment)

                    file_controller.pointer_move_absolute(begin_current_fragment)
                    file_controller.print_file()
                    unsorted_data = file_controller.read(chink_size)
                    file_controller.print_file()
                    sorted_data = list(pre_sorter(unsorted_data))

                    current_fragment_pointer = begin_current_fragment
                    last_fragment_pointer = begin_last_fragment

                    if not bool(sorted_data):
                        break
                    file_controller.pointer_move_absolute(begin_current_fragment)
                    file_controller.print_file()
                    item = sorted_data.pop(0)

                    file_controller.pointer_move_absolute(last_fragment_pointer)
                    file_controller.print_file()
                    current_item_from_last_fragment = file_controller.read()
                    file_controller.print_file()
                    last_fragment_pointer = file_controller.current_pos
                    file_controller.pointer_move_absolute(current_fragment_pointer)
                    file_controller.print_file()
                    while bool(sorted_data):
                        if item <= current_item_from_last_fragment:
                            current_fragment_pointer = file_controller.write(item)
                            file_controller.print_file()
                            item = sorted_data.pop(0)
                        else:
                            current_fragment_pointer = file_controller.write(current_item_from_last_fragment)
                            file_controller.print_file()
                            file_controller.pointer_move_absolute(last_fragment_pointer)
                            file_controller.print_file()
                            current_item_from_last_fragment = file_controller.read()
                            file_controller.print_file()
                            last_fragment_pointer = file_controller.current_pos
                            file_controller.print_file()
                            file_controller.pointer_move_absolute(current_fragment_pointer)
                            file_controller.print_file()
                    print('%'*10)
                    while True:
                        if item <= current_item_from_last_fragment:
                            current_fragment_pointer = file_controller.write(item)
                            file_controller.print_file()
                            break
                        else:
                            if (last_fragment_pointer > len_file):
                                current_item_from_last_fragment = chr(65536)
                                continue
                            current_fragment_pointer = file_controller.write(current_item_from_last_fragment)
                            file_controller.print_file()
                            file_controller.pointer_move_absolute(last_fragment_pointer)

                            file_controller.print_file()
                            current_item_from_last_fragment = file_controller.read()
                            file_controller.print_file()
                            last_fragment_pointer = file_controller.current_pos
                            file_controller.pointer_move_absolute(current_fragment_pointer)
                            file_controller.print_file()
                    # while current_fragment_pointer < last_fragment_pointer:
                    #     current_fragment_pointer = file_controller.write(current_item_from_last_fragment)
                    #     file_controller.print_file()
                    #     file_controller.pointer_move_absolute(last_fragment_pointer)
                    #     file_controller.print_file()
                    #     current_item_from_last_fragment = file_controller.read()
                    #     file_controller.print_file()
                    #     last_fragment_pointer = file_controller.current_pos
                    #     file_controller.pointer_move_absolute(current_fragment_pointer)
                    #     file_controller.print_file()





            time_ = process_time_ns() - time_
            return time_

        return selection_sort_


    def __class_getitem__(cls, data_, *item):
        print(data_, *item)
        file_control_class, internal_pre_sorter = data_
        new_cls = type(f'{cls.__name__}As{item}', (cls,), dict())
        new_cls.selection_sort = staticmethod(cls.selection_sort_producer(file_control_class, internal_pre_sorter))

        return new_cls

    @staticmethod
    def write_random_data_in_file(filename: str, len_: int = 100, data_: Optional[str] = None):
        with open(filename, 'wb') as base:
            if data_ is None:
                data_: bytes = bytes(''.join([chr(randint(ord('0'), ord('9'))) for i in range(len_)]), 'utf-8')
                base.write(data_)
            else:
                base.write((data_ if isinstance(data_, bytes) else bytes(data_, 'utf-8')))
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
            def quicksort(a: list | str):
                def _quicksort(nums):
                    if len(nums) <= 1:
                        return nums
                    else:
                        q = choice(nums)
                    l_nums = [n for n in nums if n < q]

                    e_nums = [q] * nums.count(q)
                    b_nums = [n for n in nums if n > q]
                    return _quicksort(l_nums) + e_nums + _quicksort(b_nums)

                return list(_quicksort(list(a)))

            internal_sorters: dict[cls.TypeInternalSort, Callable] = {
                cls.TypeInternalSort.none: dont_use_pre_sort,
                cls.TypeInternalSort.quick_sort: quicksort,
            }

            return internal_sorters[type_internal_sorter]




simple_file_generator = Sorts.get_file_gen()
