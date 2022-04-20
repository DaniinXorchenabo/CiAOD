from os.path import join, split
from typing import Type, Callable, Any
import enum
from os.path import join, dirname, exists, split
import os
from typing import Optional, IO, Generator, Iterable, Iterator
from random import randint
from math import log2
from itertools import islice
from functools import reduce

import uvicorn
from fastapi import FastAPI, Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sort import Sorts, simple_file_generator
from file_iter_controller import create_file_iterator_class

TypeInternalSort = Sorts.PreInternalSort.TypeInternalSort

app = FastAPI()
DATA_FILE_NAME: Optional[str] = None


class SortType(str, enum.Enum):
    selection = "selection"


def sort_func_decorator(func):
    def decorator(
            *args,
            data=None,
            get_history: bool = False,
            count_of_read: bool = False,
            count_of_write: bool = False,
            type_internal_sort: TypeInternalSort,
            chink_size_for_internal_sort: int,
            **kwargs
    ):
        Sorts.write_random_data_in_file(args[0], len_=len(data), data_=data)

        file_control_class = create_file_iterator_class(
            count_of_reads=count_of_read,
            count_of_write=count_of_write,
            get_history=get_history,
        )
        internal_sorter = Sorts.PreInternalSort.get_internal_pre_sorter(type_internal_sort,
                                                                        chink_size_for_internal_sort)

        time = func(
            file_control_class,
            internal_sorter,
            *args,
            data=data,
            chink_size_for_internal_sort=chink_size_for_internal_sort,
            **kwargs)

        _d = file_control_class.return_static_variables()

        if 'history' in _d and isinstance(_d, dict) and bool(_d['history']):
            # with open(next(iter(_d['history'])), 'r', encoding='utf-8') as f:
            #     _d['history'][f] = f.read()

            _m = [i for i in _d['history']]
            max_len_filename = len(max(_m, key=lambda i: len(i[0]))[0])
        else:
            _m = max_len_filename = None
        # print(_d)
        return {
            "time": time,
            'count_of_read': _d['count_of_reads'],
            'count_of_write': _d['count_of_writes'],
            'history': _m and '\n'.join(
                [i for i in _m])
        }

    return decorator


@sort_func_decorator
def run_selection_sorting(file_control_class, internal_sorter, *args, **kwargs):
    return Sorts[file_control_class, internal_sorter].selection_sort(*args, **kwargs)


sorts_func: dict[SortType, Callable] = {
    SortType.selection: run_selection_sorting,
}


sorts_args: dict[SortType, tuple[tuple[str, ...], dict[str, Any]]] = dict()


@app.on_event('startup')
def create_files():
    global sorts_args, DATA_FILE_NAME
    DATA_FILE_NAME, a = [
        join(dirname(__file__), 'files', i) for i in [
            'data.bin', "a.bin"]]
    sorts_args[SortType.selection] = (a,), dict()


@app.get("/", response_class=FileResponse)
async def get_ui():
    return "public/main.html"


@app.get("/get_sorts_time")
async def get_graphs_data(
        len_file: Optional[int],
        data_: Optional[str] = None,
        get_history: bool = False,
        count_of_read: bool = False,
        count_of_write: bool = False,
        external_sort_type: SortType = SortType.selection,
        type_internal_sort: TypeInternalSort = TypeInternalSort.quick_sort,
        chink_size_for_internal_sort: int = 100,

):

    assert (len_file is None or data_ is None) or len_file == len(data_)
    assert len_file is not None or data_ is not None

    data = Sorts.write_random_data_in_file(DATA_FILE_NAME, len_=len_file or len(data_), data_=data_)

    return {
        external_sort_type: sorts_func[external_sort_type](
            *sorts_args[external_sort_type][0],
            **(
                    sorts_args[external_sort_type][1]
                    | {
                        'len_file': len_file,
                        'data': data,
                        'get_history': get_history,
                        'count_of_read': count_of_read,
                        "count_of_write": count_of_write,
                        "type_internal_sort": type_internal_sort,
                        "chink_size_for_internal_sort": chink_size_for_internal_sort,

                    }
            )
        )
    }


@app.get("/get_many_sorts")
async def get_many_sorts(
        len_file: Optional[int],
        data_: Optional[str] = None,
        get_history: bool = False,
        count_of_read: bool = False,
        count_of_write: bool = False,
        external_sort_type: SortType = SortType.selection,
        type_internal_sort: TypeInternalSort = TypeInternalSort.quick_sort,
):
    assert (len_file is None or data_ is None) or len_file == len(data_)
    assert len_file is not None or data_ is not None

    data = Sorts.write_random_data_in_file(DATA_FILE_NAME, len_=len_file or len(data_), data_=data_)

    return reduce(
        lambda last, i: last | i,
        [
            {k + f"_{ind}_percent": v for k, v in (
                await get_graphs_data(
                    len_file=None,
                    data_=data,
                    get_history=get_history,
                    count_of_read=count_of_read,
                    count_of_write=count_of_write,
                    type_internal_sort=type_internal_sort,
                    external_sort_type=external_sort_type,
                    chink_size_for_internal_sort=i
                )
            ).items()}
            for ind, i in enumerate(range(len(data) // 100, len(data) // 100 * 10 + 1, len(data) // 100), 1)]
    )


@app.get("/get_files")
async def get_files_names():
    # print(*os.walk(join(dirname(__file__), 'files')), sep='\n')
    return  ['a.bin', 'data.bin']


@app.get("/get_part_file")
async def get_files_names(from_: int, to_: int, filename: str):
    with open(join(dirname(__file__), 'files', filename), 'r', encoding='utf-8') as f:
        return ' '.join([i for ind, i in islice(enumerate(simple_file_generator(f)), from_, to_)])


@app.get('/get_sort_types')
async def get_sort_types():
    return [i for i in TypeInternalSort]


app.mount("/public", StaticFiles(directory=join(split(__file__)[0], 'public')), name="static")

if __name__ == "__main__":

    # with open("files/a.txt", "r+") as f:
    #     f.seek(0, 0)
    #     f.write("t")
    #     f.write("r")
    #     f.seek(0, 0)
    #     f.write("w")


    uvicorn.run("main:app", host="localhost", port=9020, reload=True)
