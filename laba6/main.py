from os.path import join, split
from typing import Type, Callable, Any
import enum
from os.path import join, dirname, exists, split
import os
from typing import Optional, IO, Generator, Iterable, Iterator
from random import randint
from math import log2
from itertools import islice

import uvicorn
from fastapi import FastAPI, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sort import Sorts, simple_file_generator

app = FastAPI()
DATA_FILE_NAME: Optional[str] = None


class SortType(str, enum.Enum):
    two = "two"
    one = "one"


def sort_func_decorator(func):
    def decorator(*args, data=None, get_history: bool = False, count_of_read: bool = False,
                  count_of_write: bool = False, **kwargs):
        Sorts.write_random_data_in_file(args[0], len_=len(data), data_=data)

        current_file_reader = Sorts.get_file_gen(get_history=get_history, count_of_read=count_of_read)
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
def run_one_phase_sorting(current_file_reader, writer, *args, **kwargs):
    return Sorts[current_file_reader, writer].one_phase_sorting_by_simple_merge(*args, **kwargs)


@sort_func_decorator
def run_two_phase_sorting(current_file_reader, writer, *args, **kwargs):
    return Sorts[current_file_reader, writer].two_phase_sorting_by_simple_merge(*args, **kwargs)


sorts_func: dict[SortType, Callable] = {
    SortType.one: run_one_phase_sorting,
    SortType.two: run_two_phase_sorting,
}

sorts_args: dict[SortType, tuple[tuple[str, ...], dict[str, Any]]] = dict()


@app.on_event('startup')
def create_files():
    global sorts_args, DATA_FILE_NAME
    DATA_FILE_NAME, base_1, f1_b, f1_c, base_2, f2_b, f2_c, f2_d, f2_e = [
        join(dirname(__file__), 'files', i) for i in [
            'data.txt',
            'two_phase/main.txt', 'two_phase/b.txt', 'two_phase/c.txt',
            'one_phase/main.txt', 'one_phase/B.txt',
            'one_phase/C.txt', 'one_phase/D.txt', 'one_phase/E.txt']]
    sorts_args[SortType.one] = (base_2, f2_b, f2_c, f2_d, f2_e), dict()
    sorts_args[SortType.two] = (base_1, f1_b, f1_c,), dict()


@app.get("/", response_class=FileResponse)
async def get_ui():
    return "public/main.html"


@app.get("/get_sorts_time")
async def get_graphs_data(len_file: Optional[int], data_: Optional[str] = None,
                          get_history: bool = False, count_of_read: bool = False,
                          count_of_write: bool = False):
    assert (len_file is None or data_ is None) or len_file == len(data_)
    assert len_file is not None or data_ is not None
    data = Sorts.write_random_data_in_file(DATA_FILE_NAME, len_=len_file or len(data_), data_=data_)

    return {s: sorts_func[s](*sorts_args[s][0], **(sorts_args[s][1] | {
        'len_file': len_file, 'data': data, 'get_history': get_history,
        'count_of_read': count_of_read, "count_of_write": count_of_write})
                             ) for s in SortType}


@app.get("/get_files")
async def get_files_names():
    print(*os.walk(join(dirname(__file__), 'files')), sep='\n')
    return [join(split(i[0])[1], j) for i in os.walk(join(dirname(__file__), 'files'))
            if split(i[0])[1] in ['one_phase', 'two_phase'] or (split(i[0])[1] == 'files')
            for j in i[2]] + ['data.txt']


@app.get("/get_part_file")
async def get_files_names(from_: int, to_: int, filename: str):
    with open(join(dirname(__file__), 'files', filename), 'r', encoding='utf-8') as f:
        return ''.join([i for ind, i in islice(enumerate(simple_file_generator(f)), from_, to_)])


app.mount("/public", StaticFiles(directory=join(split(__file__)[0], 'public')), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=9010, reload=True)
