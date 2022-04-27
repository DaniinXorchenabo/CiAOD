from typing import Callable, Any
from os.path import split
from typing import Optional

from lab10.sorts.abstract_pre_sort import SortType
from lab10.sorts.sort import AllSorts


DATA_FILE_NAME: Optional[str] = None


def sort_func_decorator(func):
    def decorator(*args, data=None, get_history: bool = False, count_of_read: bool = False,
                  count_of_write: bool = False, **kwargs):
        AllSorts.write_random_data_in_file(args[0], len_=len(data), data_=data)

        current_file_reader = AllSorts.get_file_gen(get_history=get_history, count_of_read=count_of_read)
        writer = Sorts.get_write_file_func(count_of_write=count_of_write)

        time = func(current_file_reader, writer, *args, data=data, **kwargs)

        _d = next(current_file_reader(None, return_static_variables=True))
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
            'count_of_write': writer(None, return_static_variables=True)['count_of_write'],
            'history': _m and '\n'.join([f'{key.ljust(max_len_filename, " ")}:{val}' for [key, val] in _m])
        }

    return decorator


@sort_func_decorator
def run_one_phase_sorting(sort_class_type: SortType, current_file_reader, writer, *args, **kwargs):
    return AllSorts[sort_class_type, current_file_reader, writer].one_phase_sorting_by_simple_merge(*args, **kwargs)


@sort_func_decorator
def run_two_phase_sorting(sort_class_type: SortType, current_file_reader, writer, *args, **kwargs):
    return AllSorts[sort_class_type, current_file_reader, writer].two_phase_sorting_by_simple_merge(*args, **kwargs)


@sort_func_decorator
def run_selection_sorting(sort_class_type: SortType, file_control_class, internal_sorter, *args, **kwargs):
    return AllSorts[sort_class_type, file_control_class, internal_sorter].selection_sort(*args, **kwargs)


sorts_func: dict[SortType, Callable] = {
    SortType.one6: run_one_phase_sorting,
    SortType.two6: run_two_phase_sorting,
    SortType.one7: run_one_phase_sorting,
    SortType.two7: run_two_phase_sorting,
    SortType.one8: run_one_phase_sorting,
    SortType.two8: run_two_phase_sorting,
    SortType.selection: run_selection_sorting,
}

sorts_args: dict[SortType, tuple[tuple[str, ...], dict[str, Any]]] = dict()
