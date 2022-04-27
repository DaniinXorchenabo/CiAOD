from typing import Callable, Any
from os.path import split
from typing import Optional

from lab10.sorts.abstract_pre_sort import SortType
from lab10.sorts.file_iter_controller import create_file_iterator_class
from lab10.sorts.sort import AllSorts
from lab10.sorts.sort_lab_9 import Sorts as Sorts9
from lab10.sorts.abstract_pre_sort import AbstractPreSort


TypeInternalSort = AbstractPreSort.PreInternalSort.TypeInternalSort

DATA_FILE_NAME: Optional[str] = None


def sort_func_decorator(func):
    def decorator(
            *args,
            data=None,
            get_sort_type: SortType,
            get_history: bool = False,
            count_of_read: bool = False,
            count_of_write: bool = False,
            type_internal_sort: TypeInternalSort | None = None,
            chink_size_for_internal_sort: int | None = None,
            **kwargs):
        AllSorts.write_random_data_in_file(args[0], len_=len(data), data_=data)

        if get_sort_type == SortType.selection:

            if type_internal_sort is None or chink_size_for_internal_sort is None:
                raise AttributeError()

            file_control_class = create_file_iterator_class(
                count_of_read=count_of_read,
                count_of_write=count_of_write,
                get_history=get_history,
            )
            internal_sorter = Sorts9.PreInternalSort.get_internal_pre_sorter(
                type_internal_sort,
                chink_size_for_internal_sort
            )
            time = func(
                get_sort_type,
                file_control_class,
                internal_sorter,
                *args,
                data=data,
                chink_size_for_internal_sort=chink_size_for_internal_sort,
                **kwargs)
            _d = file_control_class.return_static_variables()
            _m = max_len_filename = None
        else:
            print(get_sort_type)
            current_file_reader = AllSorts.get_file_gen(get_history=get_history, count_of_read=count_of_read)
            writer = AllSorts.get_write_file_func(count_of_write=count_of_write)

            if get_sort_type in [SortType.one8, SortType.two8]:
                if chink_size_for_internal_sort is None:
                    raise AttributeError()
                internal_sorter = AbstractPreSort.PreInternalSort.get_internal_pre_sorter(type_internal_sort,
                                                                                chink_size_for_internal_sort)
                args = (internal_sorter, *args)

            time = func(get_sort_type, current_file_reader, writer, *args, data=data, **kwargs)
            _d = next(current_file_reader(None, return_static_variables=True))
            _d |= writer(None, return_static_variables=True)

            if 'history' in _d and isinstance(_d, dict) and bool(_d['history']):
                with open(next(iter(_d['history'])).name, 'r', encoding='utf-8') as f:
                    _d['history'][f] = f.read()
                    _m = [(split(key.name)[-1], val) for key, val in _d['history'].items()]
                    max_len_filename = len(max(_m, key=lambda i: len(i[0]))[0])
            else:
                _m = max_len_filename = None

        return {
            "time": time,
            'count_of_read': _d['count_of_read'],
            'count_of_write': _d['count_of_write'],
            'history': _m and '\n'.join([f'{key.ljust(max_len_filename, " ")}:{val}' for [key, val] in _m])
        }

    return decorator


@sort_func_decorator
def run_one_phase_sorting6(sort_class_type: SortType, current_file_reader, writer, *args, **kwargs):
    return AllSorts[sort_class_type, current_file_reader, writer].one_phase_sorting_by_simple_merge(*args, **kwargs)


@sort_func_decorator
def run_two_phase_sorting6(sort_class_type: SortType, current_file_reader, writer, *args, **kwargs):
    print(AllSorts[sort_class_type, current_file_reader, writer])
    return AllSorts[sort_class_type, current_file_reader, writer].two_phase_sorting_by_simple_merge(*args, **kwargs)


@sort_func_decorator
def run_one_phase_sorting7(sort_class_type: SortType, current_file_reader, writer, *args, **kwargs):
    return AllSorts[ sort_class_type, current_file_reader, writer].one_phase_sorting_by_natural_merge(*args, **kwargs)


@sort_func_decorator
def run_two_phase_sorting7(sort_class_type: SortType, current_file_reader, writer, *args, **kwargs):
    print(AllSorts[ sort_class_type, current_file_reader, writer])
    return AllSorts[ sort_class_type, current_file_reader, writer].two_phase_sorting_by_natural_merge(*args, **kwargs)


@sort_func_decorator
def run_one_phase_sorting8(sort_class_type: SortType, current_file_reader, writer, internal_sorter, *args, **kwargs):
    return AllSorts[ sort_class_type, current_file_reader, writer,internal_sorter].internal_sorting_with_one_phase_natural_merge(*args, **kwargs)


@sort_func_decorator
def run_two_phase_sorting8(sort_class_type: SortType, current_file_reader, writer, internal_sorter, *args, **kwargs):
    return AllSorts[ sort_class_type, current_file_reader, writer, internal_sorter].internal_sorting_with_two_phase_natural_merge(*args, **kwargs)


@sort_func_decorator
def run_selection_sorting(sort_class_type: SortType, file_control_class, internal_sorter, *args, **kwargs):
    return AllSorts[ sort_class_type, file_control_class, internal_sorter].selection_sort(*args, **kwargs)


sorts_func: dict[SortType, Callable] = {
    SortType.one6: run_one_phase_sorting6,
    SortType.two6: run_two_phase_sorting6,
    SortType.one7: run_one_phase_sorting7,
    SortType.two7: run_two_phase_sorting7,
    SortType.one8: run_one_phase_sorting8,
    SortType.two8: run_two_phase_sorting8,
    SortType.selection: run_selection_sorting,
}

sorts_args: dict[SortType, tuple[tuple[str, ...], dict[str, Any]]] = dict()
