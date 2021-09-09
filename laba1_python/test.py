#!/usr/bin/env python3
from array import array, ArrayType
from time import time
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, VerticalDivider, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from asciimatics.widgets.frame import THEMES
from asciimatics.widgets.popupdialog import PopUpDialog
import sys
import sqlite3
from random import random, randint, shuffle
from itertools import chain
from collections import defaultdict
from asciimatics.renderers import FigletText, Fire
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
from pyfiglet import Figlet
import sys

# arr = list(range(10))
# sorted_arr = list(range(10))
# shuffle(arr)
# print(arr)
# print(sorted_arr)

arr = array("Q", (_arr := list(chain(*[range(3 * int(10e5)) for i in range(1)]))))
shuffle(arr)

sorted_arr = _arr + list(chain(*[range(3 * int(10e5), 6 * int(10e5)) for i in range(1)]))
shuffle(sorted_arr)
sorted_arr = sorted_arr[int(3 * 10e5):]
sorted_arr.sort()
sorted_arr = array("Q", sorted_arr)


THEMES.update(
    {"my_theme": defaultdict(
        lambda: (Screen.COLOUR_WHITE, Screen.A_NORMAL, 	234),
        {
            "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, 	234),
            "background_menu": (Screen.COLOUR_WHITE, Screen.A_NORMAL, 	236),
            "invalid": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_RED),
            "label": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            "focus_button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            "selected_focus_control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLACK),
            "disabled": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
        }
    )}
)


class ContactModel(object):
    def __init__(self):
        # Create a database in RAM.
        self._db = sqlite3.connect(':memory:')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        self._db.cursor().execute('''
            CREATE TABLE contacts(
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                address TEXT,
                email TEXT,
                notes TEXT)
        ''')
        self._db.commit()

        # Current contact when editing.
        self.current_id = None

    def add(self, contact):
        self._db.cursor().execute('''
            INSERT INTO contacts(name, phone, address, email, notes)
            VALUES(:name, :phone, :address, :email, :notes)''',
                                  contact)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT name, id from contacts").fetchall()

    def get_contact(self, contact_id):
        return self._db.cursor().execute(
            "SELECT * from contacts WHERE id=:id", {"id": contact_id}).fetchone()

    def get_current_contact(self):
        if self.current_id is None:
            return {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
        else:
            return self.get_contact(self.current_id)

    def update_current_contact(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE contacts SET name=:name, phone=:phone, address=:address,
                email=:email, notes=:notes WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_contact(self, contact_id):
        self._db.cursor().execute('''
            DELETE FROM contacts WHERE id=:id''', {"id": contact_id})
        self._db.commit()


class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Contact List")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.get_summary(),
            name="contacts",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self._edit)
        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self._edit_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self._edit_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["contacts"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class ContactView(Frame):
    def __init__(self, screen, model):
        super(ContactView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Contact Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Address:", "address"))
        layout.add_widget(Text("Phone number:", "phone"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()
        # 161415 - фон

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ContactView, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class ChangingLabel(Label):

    def __init__(self, label, *a, **k):
        super().__init__(label, *a, **k)
        self._start_text = label

    def change_text(self, add_text: str):
        self._text = self._start_text + add_text


class MyView(Frame):
    def __init__(self, screen, model):
        super(MyView, self).__init__(screen,
                                     screen.height * 2 // 3,
                                     screen.width * 2 // 3,
                                     on_load=self._reload_list,
                                     hover_focus=True,
                                     can_scroll=False,
                                     title="Последовательный поиск")
        # Save off the model that accesses the contacts database.
        self.set_theme("bright")
        self._model = model
        title_layout = Layout([110])
        self.add_layout(title_layout)
        title_layout.add_widget(Divider())
        layout = Layout([50, 10, 50], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Label("Неупорядоченный массив"))
        layout.add_widget(Divider())
        layout.add_widget(Text("Ищем число:", "key_1", validator="^[0-9]{1,}$"))
        layout.add_widget(Label(""))
        layout.add_widget(Label("Неоптимальный поиск"))
        layout.add_widget(Label(""))
        self.time_1_no = ChangingLabel("Время :")
        self.index_1_no = ChangingLabel("Индекс:")
        layout.add_widget(self.time_1_no)
        layout.add_widget(self.index_1_no)
        layout.add_widget(Label(""))
        layout.add_widget(Label("Оптимальный поиск"), column=0)
        layout.add_widget(Label(""))
        self.time_1_opt = ChangingLabel("Время :")
        self.index_1_opt = ChangingLabel("Индекс:")
        layout.add_widget(self.time_1_opt)
        layout.add_widget(self.index_1_opt)
        layout.add_widget(Divider())
        layout.add_widget(Button("Найти", self.generate_1), column=0)

        layout.add_widget(VerticalDivider(), column=1)

        layout.add_widget(Label("Упорядоченный массив"), column=2)
        layout.add_widget(Divider(), column=2)
        layout.add_widget(Text("Ищем число:", "key_2", validator="^[0-9]{1,}$"), column=2)
        layout.add_widget(Label(""), column=2)
        layout.add_widget(Label("Поиск как в неупорядоченном"), column=2)
        layout.add_widget(Label(""), column=2)
        self.time_2_no = ChangingLabel("Время :")
        self.index_2_no = ChangingLabel("Индекс:")
        layout.add_widget(self.time_2_no, column=2)
        layout.add_widget(self.index_2_no, column=2)
        layout.add_widget(Label(""), column=2)
        layout.add_widget(Label("Поиск как в упорядоченном"), column=2)
        layout.add_widget(Label(""), column=2)
        self.time_2_up = ChangingLabel("Время :")
        self.index_2_up = ChangingLabel("Индекс:")
        layout.add_widget(self.time_2_up, column=2)
        layout.add_widget(self.index_2_up, column=2)
        layout.add_widget(Divider(), column=2)
        layout.add_widget(Button("Найти", self.generate_2), column=2)

        layout_footer = Layout([1])
        self.add_layout(layout_footer)
        layout_footer.add_widget(Divider())
        layout_footer.add_widget(Button("Quit", self._quit), 0)
        self.fix()

    def _reload_list(self, new_value=None):
        # self._list_view.options = self._model.get_summary()
        # self._list_view.value = new_value
        pass

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

    def generate_1(self):
        # shuffle(arr)
        self.save()
        try:
            key = int(self.data["key_1"])

            # PopUpDialog()
            ind1, time1 = self.no_opt_find(key, arr)
            ind2, time2 = self.opt_find(key, arr)
            # print(ind1, time1, ind2, time2)
        except (TypeError, ValueError):
            ind1 = time1 = ind2 = time2 = "некорректный ввод"
        self.time_1_no.change_text(str(time1))
        self.time_1_opt.change_text(str(time2))
        self.index_1_no.change_text(str(ind1))
        self.index_1_opt.change_text(str(ind2))
        self.time_1_no.update(None)

    def generate_2(self):
        self.save()
        try:
            key = int(self.data["key_2"])
            ind1, time1 = self.opt_find(key, sorted_arr)
            ind2, time2 = self.up_find(key, sorted_arr)
            print(ind1, time1, ind2, time2)

        except (TypeError, ValueError):
            ind1 = time1 = ind2 = time2 = "некорректный ввод"

        self.time_2_no.change_text(str(time1))
        self.time_2_up.change_text(str(time2))
        self.index_2_no.change_text(str(ind1))
        self.index_2_up.change_text(str(ind2))
        self.time_1_no.update(None)

    @staticmethod
    def no_opt_find(element: int, arr: ArrayType) -> tuple[str, float]:
        element = int(element)
        i: int = 0
        len_ = len(arr)
        start = time()
        while i != len_:
            if element == arr[i]:
                break
            i += 1
        end = time()
        if i == len_:
            i: str = "Не найдено"
        return str(i), end - start

    @staticmethod
    def opt_find(element: int, loc_arr: ArrayType) -> tuple[str, float]:
        element = int(element)
        i: int = 0
        loc_arr.append(element)
        start = time()
        while element != loc_arr[i]:
            i += 1
        if i == len(loc_arr) - 1:
            i: str = "Не найдено"
        end = time()
        loc_arr.pop(len(loc_arr) - 1)
        return str(i), end - start

    @staticmethod
    def up_find(element: int, loc_arr: ArrayType) -> tuple[str, float]:
        element = int(element)
        i: int = 0
        loc_arr.append(element + 1)
        start = time()
        while element > loc_arr[i]:
            i += 1
        if loc_arr[i] != element:
            i: str = "Не найдено"
        end = time()
        loc_arr.pop(len(loc_arr) - 1)
        return str(i), end - start


def demo(screen, scene):
    fire = Print(screen,
          Fire(screen.height, screen.width, "*" * (screen.width - 20), 0.8, 60, screen.colours,
               bg=screen.colours >= 256),
          0,
          speed=1,
          transparent=False)

    scenes = [
        Scene([
            fire,
            MyView(screen, contacts)
        ], 500, name="Main"),
        # Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


contacts = ContactModel()
last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
