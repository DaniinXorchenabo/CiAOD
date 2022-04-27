from abc import ABC
from random import randint
from typing import Optional, IO


class AbstractSort(ABC):

    @staticmethod
    def write_random_data_in_file(filename: str, len_: int = 100, data_: Optional[str] = None):
        if filename.endswith('.bin'):
            with open(filename, 'wb') as base:
                if data_ is None:
                    data_: bytes = bytes(''.join([chr(randint(ord('0'), ord('9'))) for i in range(len_)]), 'utf-8')
                    base.write(data_)
                else:
                    print(type(data_))
                    if isinstance(data_, bytes) is False:
                        data_: bytes = bytes(data_, 'utf-8')
                        print("**", type(data_))
                    print("&&&:", type(data_))
                    base.write(data_)
        else:
            with open(filename, 'w', encoding='utf-8') as base:
                if data_ is None:
                    data_: str = ''.join([chr(randint(ord('0'), ord('9'))) for i in range(len_)])
                    print(data_, end='', sep='', file=base)
                else:
                    print(data_, end='', sep='', file=base)
        return data_

    @staticmethod
    def get_file_gen(get_history: bool = False, count_of_read: bool = False, **useless_kwargs):
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
    def get_write_file_func(count_of_write: bool = False, **useless_kwargs):
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

    def __class_getitem__(cls, data_, *item):
        new_cls = type(f'{cls.__name__}As{item}', (cls,), dict())
        return new_cls
