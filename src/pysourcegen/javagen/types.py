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
from pysourcegen.javagen.item import JavaItem


def _List(names: Union[str, List[str], None]) -> str:
    if not names:
        return ''
    return names if isinstance(names, str) else ', '.join(names)


class _Line(JavaItem, TextBase):
    pass


class _TypeDeclaration(JavaItem):

    KEYWORD = 'class'

    def __init__(self, name: str, modifiers: str):
        super().__init__()
        self._name = name
        self._modifiers = modifiers
        self._items = []

    def AddField(self, typename: str, name: str, value: Optional[str] = None,
                 modifiers: str = 'private') -> None:
        """Add ``modifiers typename name = value;``."""
        field = JoinWords(modifiers, typename, name)
        if value is not None:
            field += f' = {value}'
        self._items.append(_Line(field + ';'))

    def Add(self, item: JavaItem) -> None:
        self._items.append(item)

    def _Header(self) -> str:
        return JoinWords(self._modifiers, self.KEYWORD, self._name)

    def __str__(self) -> str:
        return self.RenderBlock(self._Header(), self._items) + '\n'


class JavaClass(_TypeDeclaration):
    """``modifiers class name extends base implements interfaces { ... }``.
    ``implements`` is a name or a list of names."""

    def __init__(self, name: str, modifiers: str = 'public',
                 extends: Optional[str] = None,
                 implements: Union[str, List[str], None] = None):
        super().__init__(name, modifiers)
        self.__extends = extends
        self.__implements = _List(implements)

    def _Header(self) -> str:
        return JoinWords(
            super()._Header(),
            f'extends {self.__extends}' if self.__extends else '',
            f'implements {self.__implements}' if self.__implements else '')


class JavaInterface(_TypeDeclaration):
    """``modifiers interface name extends bases { ... }``. Add methods
    without a body with ``Add(JavaMethod(name, type, None, modifiers=''))``."""

    KEYWORD = 'interface'

    def __init__(self, name: str, modifiers: str = 'public',
                 extends: Union[str, List[str], None] = None):
        super().__init__(name, modifiers)
        self.__extends = _List(extends)

    def _Header(self) -> str:
        return JoinWords(
            super()._Header(),
            f'extends {self.__extends}' if self.__extends else '')


class JavaEnum(_TypeDeclaration):
    """``modifiers enum name { ... }``. Constants come first, then any
    fields, constructors and methods added with ``AddField`` or ``Add``."""

    KEYWORD = 'enum'

    def __init__(self, name: str, modifiers: str = 'public'):
        super().__init__(name, modifiers)
        self.__constants = []

    def AddConstant(self, name: str, args: Optional[str] = None) -> None:
        """Add ``name``, or ``name(args)`` when ``args`` is given."""
        self.__constants.append(name if args is None else f'{name}({args})')

    def __str__(self) -> str:
        items = []
        if self.__constants:
            # Constants are separated by commas. A semicolon ends the list
            # when members follow.
            last = ';' if self._items else ','
            items = [_Line(c + ',') for c in self.__constants[:-1]]
            items.append(_Line(self.__constants[-1] + last))
            if self._items:
                items.append(_Line(''))
        return self.RenderBlock(self._Header(), items + self._items) + '\n'
