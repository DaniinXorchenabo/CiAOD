import enum
from itertools import islice
from random import choice
from typing import Callable, Generator

from lab10.sorts.abstract_sort import AbstractSort


class AbstractPreSort(AbstractSort):
    class PreInternalSort(object):

        class TypeInternalSort(str, enum.Enum):
            quick_sort = "quick_sort"
            none = "none"

        @staticmethod
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


class SortType(str, enum.Enum):
    two6 = "two6"
    one6 = "one6"
    two7 = "two7"
    one7 = "one7"
    two8 = "two8"
    one8 = "one8"
    selection9 = "selection9"