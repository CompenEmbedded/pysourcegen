# Copyright 2024 Compen Embedded B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, Union

from pysourcegen.common import JoinWords, TextBase
from pysourcegen.jsgen.item import Export, JsItem, Typed


def _List(names: Union[str, List[str], None]) -> str:
    if not names:
        return ''
    return names if isinstance(names, str) else ', '.join(names)


class _Line(JsItem, TextBase):
    pass


class JsClass(JsItem):
    """``class name extends base implements interfaces { ... }``.

    ``implements`` (TypeScript) is a name or a list of names. ``export``
    may be ``True`` or ``'default'``. Add methods with ``Add(JsMethod(...))``.
    """

    def __init__(self, name: str, extends: Optional[str] = None,
                 implements: Union[str, List[str], None] = None,
                 export: Union[bool, str] = False):
        super().__init__()
        self.__name = name
        self.__extends = extends
        self.__implements = _List(implements)
        self.__export = export
        self.__items = []

    def AddField(self, name: str, typename: Optional[str] = None,
                 value: Optional[str] = None, modifiers: str = '') -> None:
        """Add ``modifiers name: typename = value;``. Only ``name`` is
        required. ``modifiers`` is e.g. ``'static'``, ``'readonly'`` or
        ``'private'`` (TypeScript), or use a name like ``'#count'`` for a
        JavaScript private field."""
        field = JoinWords(modifiers, Typed(name, typename))
        if value is not None:
            field += f' = {value}'
        self.__items.append(_Line(field + ';'))

    def Add(self, item: JsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = JoinWords(
            Export(self.__export), 'class', self.__name,
            f'extends {self.__extends}' if self.__extends else '',
            f'implements {self.__implements}' if self.__implements else '')
        return self.RenderBlock(header, self.__items) + '\n'


class JsInterface(JsItem):
    """A TypeScript ``interface name extends bases { ... }``."""

    def __init__(self, name: str,
                 extends: Union[str, List[str], None] = None,
                 export: Union[bool, str] = False):
        super().__init__()
        self.__name = name
        self.__extends = _List(extends)
        self.__export = export
        self.__items = []

    def AddMember(self, name: str, typename: str,
                  optional: bool = False) -> None:
        """Add ``name: typename;``, or ``name?: typename;`` if optional.
        For a method, pass e.g. ``AddMember('area()', 'number')``."""
        self.__items.append(
            _Line(f'{name}{"?" if optional else ""}: {typename};'))

    def Add(self, item: JsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = JoinWords(
            Export(self.__export), 'interface', self.__name,
            f'extends {self.__extends}' if self.__extends else '')
        return self.RenderBlock(header, self.__items) + '\n'


class JsEnum(JsItem):
    """A TypeScript ``enum name { ... }``, or ``const enum`` if
    ``const`` is set."""

    def __init__(self, name: str, export: bool = False, const: bool = False):
        super().__init__()
        self.__name = name
        self.__export = export
        self.__const = const
        self.__items = []

    def AddMember(self, name: str, value: Optional[object] = None) -> None:
        """Add ``name,`` or ``name = value,``. Pass string values with their
        quotes, e.g. ``AddMember('Red', '"red"')``."""
        self.__items.append(
            _Line(f'{name},' if value is None else f'{name} = {value},'))

    def Add(self, item: JsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = JoinWords(Export(self.__export),
                           'const' if self.__const else '', 'enum',
                           self.__name)
        return self.RenderBlock(header, self.__items) + '\n'
