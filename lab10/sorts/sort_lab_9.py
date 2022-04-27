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
from lab10.sorts.file_iter_controller import FileIteratorAbstract
from lab10.sorts.abstract_sort import AbstractSort

from lab10.sorts.abstract_pre_sort import AbstractPreSort


TypeInternalSort = AbstractPreSort.PreInternalSort.TypeInternalSort


class Sorts(AbstractPreSort):
    selection_sort: Callable

    @classmethod
    def selection_sort_producer(cls, file_control_class: Type[FileIteratorAbstract], pre_sorter, *args):

        def selection_sort_(
                base_file: str,
                *args,
                len_file: Optional[int] = None,
                chink_size_for_internal_sort: int = 1,
                **kwargs
        ):
            chink_size = chink_size_for_internal_sort
            print(chink_size)
            if len_file is None:
                with open(base_file, 'rb') as base:
                    len_file = len(base.read())

            time_ = process_time_ns()

            begin_current_fragment = len_file
            begin_last_fragment = len_file
            with open(base_file, 'rb+') as base:

                file_controller = file_control_class(base)
                file_controller.move_to_tail()

                begin_last_fragment = begin_current_fragment
                begin_current_fragment -= chink_size
                file_controller.pointer_move_absolute(begin_current_fragment)

                unsorted_data: str = file_controller.read(chink_size)

                sorted_data = list(pre_sorter(unsorted_data))
                file_controller.show_op(sorted_data)
                file_controller.pointer_move_relative(-chink_size)

                file_controller.write(sorted_data)
                file_controller.show_op([])

                # print('='*10)
                while begin_current_fragment > 0:

                    begin_last_fragment = begin_current_fragment
                    begin_current_fragment -= chink_size
                    _begin_current_fragment = begin_current_fragment
                    begin_current_fragment = max(0, begin_current_fragment)
                    chink_size = chink_size + (_begin_current_fragment - begin_current_fragment)

                    file_controller.pointer_move_absolute(begin_current_fragment)

                    unsorted_data = file_controller.read(chink_size)

                    sorted_data = list(pre_sorter(unsorted_data))
                    file_controller.show_op(sorted_data)

                    current_fragment_pointer = begin_current_fragment
                    last_fragment_pointer = begin_last_fragment

                    if not bool(sorted_data):
                        break
                    file_controller.pointer_move_absolute(begin_current_fragment)

                    item = sorted_data.pop(0)

                    file_controller.pointer_move_absolute(last_fragment_pointer)

                    current_item_from_last_fragment = file_controller.read()

                    last_fragment_pointer = file_controller.current_pos
                    file_controller.pointer_move_absolute(current_fragment_pointer)

                    while bool(sorted_data):
                        if item <= current_item_from_last_fragment:
                            current_fragment_pointer = file_controller.write(item)

                            file_controller.show_op(sorted_data)
                            item = sorted_data.pop(0)
                        else:
                            if (last_fragment_pointer > len_file):
                                current_item_from_last_fragment = chr(65536)
                                continue
                            current_fragment_pointer = file_controller.write(current_item_from_last_fragment)

                            file_controller.pointer_move_absolute(last_fragment_pointer)

                            current_item_from_last_fragment = file_controller.read()

                            last_fragment_pointer = file_controller.current_pos

                            file_controller.pointer_move_absolute(current_fragment_pointer)

                    # print('%'*10)
                    while True:
                        if item <= current_item_from_last_fragment:
                            current_fragment_pointer = file_controller.write(item)
                            file_controller.show_op([])

                            break
                        else:
                            if (last_fragment_pointer > len_file):
                                current_item_from_last_fragment = chr(65536)
                                continue
                            current_fragment_pointer = file_controller.write(current_item_from_last_fragment)

                            file_controller.pointer_move_absolute(last_fragment_pointer)

                            current_item_from_last_fragment = file_controller.read()

                            last_fragment_pointer = file_controller.current_pos
                            file_controller.pointer_move_absolute(current_fragment_pointer)

            time_ = process_time_ns() - time_
            return time_

        return selection_sort_

    def __class_getitem__(cls, data_, *item):
        print(data_, *item)
        sort_class_type, file_control_class, internal_pre_sorter = data_
        new_cls = super().__class_getitem__(data_, *item)
        new_cls.selection_sort = staticmethod(cls.selection_sort_producer(file_control_class, internal_pre_sorter))

        return new_cls

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
                cls.TypeInternalSort.quick_sort: cls.quicksort,
            }

            return internal_sorters[type_internal_sorter]
