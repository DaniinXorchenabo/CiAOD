from typing import IO, Type
from abc import ABC, abstractmethod, abstractstaticmethod


class FileIteratorAbstract(ABC):

    def __init__(self, file_io: IO):
        self.file_io = file_io
        self.file_io.seek(0, 0)
        self.current_pos = 0

    @abstractmethod
    def pointer_move_absolute(self, new_position: int):
        self.file_io.seek(new_position, 0)
        self.current_pos = new_position
        return self.current_pos

    @abstractmethod
    def pointer_move_relative(self, setup: int):
        self.file_io.seek(setup, 1)
        self.current_pos += setup
        return self.current_pos

    @abstractmethod
    def write(self, char: str | list[str]):
        self.file_io.write(bytes((''.join(char) if isinstance(char, list) else char), 'utf-8'))
        self.current_pos += len(char)
        return self.current_pos

    @abstractmethod
    def read(self, count_chars: int = 1) -> str:
        data: bytes = self.file_io.read(count_chars)
        self.current_pos += count_chars
        return data.decode('utf-8')

    def read_from(self, start_char: int, count_chars: int = 1):
        cursor = self.current_pos
        self.pointer_move_absolute(start_char)
        data: str = self.read(count_chars)
        self.pointer_move_absolute(cursor)
        return data

    @abstractmethod
    def move_to_tail(self):
        self.file_io.seek(0, 2)
        self.current_pos = self.file_io.tell()
        return self.current_pos

    def change_char(self, new_char: str):
        count_of_chars = len(new_char)
        old_chars = self.read(count_of_chars)
        # print(old_chars, self.current_pos)
        self.pointer_move_relative(-count_of_chars)
        self.write(new_char)
        return old_chars

    def print_file(self):
        cursor = self.current_pos
        self.file_io.seek(0, 0)
        # st = list(" " + " ".join(list(self.file_io.read().decode('utf-8'))) + "- - - - - - - - - - - ")
        # st[cursor * 2] = "*"
        # print(''.join(st))
        self.file_io.seek(cursor, 0)

    @staticmethod
    @abstractmethod
    def return_static_variables():
        pass

    @abstractmethod
    def show_op(self, sorted_array: list):
        pass


def create_file_iterator_class(
        count_of_read: bool = False,
        count_of_write: bool = False,
        get_history: bool = False,
) -> Type[FileIteratorAbstract]:
    static_variables = {"count_of_read": 0, "count_of_write": 0, 'history': []}

    def get_history_func(self: FileIteratorAbstract):
        cursor = self.current_pos
        self.file_io.seek(0, 0)
        st = list(" " + " ".join(list(self.file_io.read().decode('utf-8'))))

        if cursor * 2 >= len(st):
            st += ["*"]
        else:
            st[cursor * 2] = "*"
        data = ''.join(st)
        self.file_io.seek(cursor, 0)
        return data

    class _FileIterator(FileIteratorAbstract):
        def read(self, count_chars: int = 1, __static_variables: dict[str, list[str]] = static_variables):
            data = super().read(count_chars)
            static_variables['history'].append(get_history_func(self))
            return data

        def write(self, char: str | list[str], __static_variables: dict[str, list[str]] = static_variables):
            data = super().write(char)
            static_variables['history'].append(get_history_func(self))
            return data

    ParentClass: Type[FileIteratorAbstract] = (_FileIterator if get_history is True else FileIteratorAbstract)

    class FileIterator(ParentClass, ABC):

        @staticmethod
        def return_static_variables():
            return static_variables

        if count_of_read is True:
            def read(self, count_chars: int = 1, __static_variables: dict[str, int] = static_variables):
                static_variables["count_of_read"] += count_chars
                return super().read(count_chars)
        else:
            def read(self, count_chars: int = 1):
                return super().read(count_chars)

        if count_of_write is True:
            def write(self, char: str | list[str], __static_variables: dict[str, int] = static_variables):
                static_variables['count_of_write'] += len(''.join(char)) if isinstance(char, list) else len(char)
                return super().write(char)
        else:
            def write(self, char: str | list[str]):
                return super().write(char)

        if get_history is True:
            def pointer_move_absolute(self, new_position: int, __static_variables: dict[str, list[str]] = static_variables):
                data = super().pointer_move_absolute(new_position)
                static_variables['history'].append(get_history_func(self))
                return data

            def pointer_move_relative(self, setup: int, __static_variables: dict[str, list[str]] = static_variables):
                data = super().pointer_move_relative(setup)
                static_variables['history'].append(get_history_func(self))
                return data

            def move_to_tail(self, __static_variables: dict[str, list[str]] = static_variables):
                data = super().move_to_tail()
                static_variables['history'].append(get_history_func(self))
                return data

            def show_op(self, sorted_array: list, __static_variables: dict[str, list[str]] = static_variables):
                if bool(__static_variables['history']):
                    __static_variables['history'][-1] += "\t<OP:" + str(sorted_array) + ">"
                else:
                    __static_variables['history'].append("\t<OP:" + str(sorted_array) + ">")

        else:
            def pointer_move_absolute(self, new_position: int):
                return super().pointer_move_absolute(new_position)

            def pointer_move_relative(self, setup: int):
                return super().pointer_move_relative(setup)

            def move_to_tail(self):
                return super().move_to_tail()

            def show_op(self, sorted_array: list):
                pass

    return FileIterator


