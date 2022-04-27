from lab10.sorts.abstract_pre_sort import SortType
from lab10.sorts.sort_lab_6 import Sorts as Sorts6
from lab10.sorts.sort_lab_7 import Sorts as Sorts7
from lab10.sorts.sort_lab_8 import Sorts as Sorts8
from lab10.sorts.sort_lab_9 import Sorts as Sorts9


class AllSorts(Sorts6, Sorts7, Sorts8, Sorts9):

    def __class_getitem__(cls, item, *data):
        class_type, *other = item
        class_type: SortType
        if class_type in [SortType.two6, SortType.one6]:
            new_cls = Sorts6.__class_getitem__(other, *data)
        elif class_type in [SortType.two7, SortType.one7]:
            new_cls = Sorts7.__class_getitem__(other, *data)
        elif class_type in [SortType.two8, SortType.one8]:
            new_cls = Sorts8.__class_getitem__(other, *data)
        elif class_type == SortType.selection:
            new_cls = Sorts9.__class_getitem__(other, *data)
        else:
            raise AttributeError(f"Некорректный тим {class_type}")
        return new_cls


simple_file_generator = AllSorts.get_file_gen()
