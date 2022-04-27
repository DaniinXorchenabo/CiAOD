from typing import Callable, Any
import enum
from os.path import join, dirname, split
import os
from typing import Optional
from itertools import islice
from functools import reduce

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from lab10.sorts.sort import AllSorts, simple_file_generator
from lab10.sort_creator import run_one_phase_sorting, run_two_phase_sorting, sorts_func, sorts_args
from lab10.sorts.abstract_pre_sort import SortType

TypeInternalSort = AllSorts.PreInternalSort.TypeInternalSort

app = FastAPI()
DATA_FILE_NAME: Optional[str] = None


@app.on_event('startup')
async def create_files():
    global sorts_args, DATA_FILE_NAME

    DATA_FILE_NAME = join(dirname(__file__), 'files', "data.txt")

    files: list[str] = await get_files_names()
    for sort_type in SortType:
        sort_type: SortType
        # sort_type.value
        type_ = str(sort_type.value)[:-1]
        lab_num = str(sort_type.value)[-1]
        dir_name = f"{type_}_phase_{lab_num}"
        if lab_num.isdigit() is False:
            dir_name = f"{sort_type.value}_9"
        file_name = join(dirname(__file__), 'files', dir_name)
        print(file_name, "|==>", list(os.walk(file_name)))
        # files: list[str] = list(os.walk(join(dirname(__file__), 'files', dir_name)))[0]
        files: list[str] = list(os.walk(join(dirname(__file__), 'files', dir_name)))[0][2]
        sorts_args[sort_type] = tuple([files[-1]] + files[:-1]), dict()

    print(*sorts_args.items(), sep='\n')


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
        external_sort_type: SortType = SortType.one6,
        type_internal_sort: TypeInternalSort = TypeInternalSort.quick_sort,
        chink_size_foe_internal_sort: int = 100,

):
    assert (len_file is None or data_ is None) or len_file == len(data_)
    assert len_file is not None or data_ is not None

    data = AllSorts.write_random_data_in_file(DATA_FILE_NAME, len_=len_file or len(data_), data_=data_)

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
                        "chink_size_foe_internal_sort": chink_size_foe_internal_sort,

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
        external_sort_type: SortType = SortType.one6,
        type_internal_sort: TypeInternalSort = TypeInternalSort.quick_sort,
):
    assert (len_file is None or data_ is None) or len_file == len(data_)
    assert len_file is not None or data_ is not None

    data = AllSorts.write_random_data_in_file(DATA_FILE_NAME, len_=len_file or len(data_), data_=data_)

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
                    external_sort_type=external_sort_type,
                    type_internal_sort=type_internal_sort,
                    chink_size_foe_internal_sort=i
                )
            ).items()}
            for ind, i in enumerate(range(len(data) // 100, len(data) // 100 * 10 + 1, len(data) // 100), 1)]
    )


@app.get("/get_files")
async def get_files_names():
    # print(*os.walk(join(dirname(__file__), 'files')), sep='\n')
    return [join(split(i[0])[1], j) for i in os.walk(join(dirname(__file__), 'files'))
            if any(split(i[0])[1].startswith(k) for k in ['one_phase', 'two_phase', "selection"])
            or (split(i[0])[1] == 'files') for j in i[2]] + ['data.txt']


@app.get("/get_part_file")
async def get_part_file(from_: int, to_: int, filename: str):
    with open(join(dirname(__file__), 'files', filename), 'r', encoding='utf-8') as f:
        return ' '.join([i for ind, i in islice(enumerate(simple_file_generator(f)), from_, to_)])


@app.get('/get_sort_types')
async def get_sort_types():
    return [i for i in TypeInternalSort]


app.mount("/public", StaticFiles(directory=join(split(__file__)[0], 'public')), name="static")

if __name__ == "__main__":
    # print(*os.walk(join(dirname(__file__), 'files')), sep='\n')
    uvicorn.run("main:app", host="localhost", port=9020, reload=True)
