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
from pysourcegen.csgen.item import CsItem


class _Line(CsItem, TextBase):
    pass


class CsClass(CsItem):
    """``modifiers class name : bases { ... }``. ``bases`` is a name or a
    list of names (base class and interfaces)."""

    KEYWORD = 'class'

    def __init__(self, name: str, modifiers: str = 'public',
                 bases: Union[str, List[str], None] = None):
        super().__init__()
        self.__name = name
        self.__modifiers = modifiers
        if isinstance(bases, str):
            bases = [bases]
        self.__bases = ', '.join(bases or [])
        self.__items = []

    def AddField(self, typename: str, name: str, value: Optional[str] = None,
                 modifiers: str = 'private') -> None:
        """Add ``modifiers typename name = value;``."""
        field = JoinWords(modifiers, typename, name)
        if value is not None:
            field += f' = {value}'
        self.__items.append(_Line(field + ';'))

    def AddProperty(self, typename: str, name: str,
                    accessors: str = 'get; set;',
                    value: Optional[str] = None,
                    modifiers: str = 'public') -> None:
        """Add an auto-property: ``modifiers typename name { accessors }``,
        followed by ``= value;`` when ``value`` is given."""
        prop = JoinWords(modifiers, typename, name, f'{{ {accessors} }}')
        if value is not None:
            prop += f' = {value};'
        self.__items.append(_Line(prop))

    def Add(self, item: CsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = JoinWords(self.__modifiers, self.KEYWORD, self.__name,
                           f': {self.__bases}' if self.__bases else '')
        return self.RenderBlock(header, self.__items) + '\n'


class CsStruct(CsClass):
    """``modifiers struct name : interfaces { ... }``."""

    KEYWORD = 'struct'


class CsInterface(CsClass):
    """``modifiers interface name : bases { ... }``. Add methods without a
    body with ``Add(CsMethod(name, type, None, modifiers=''))``."""

    KEYWORD = 'interface'


class CsEnum(CsItem):
    """``modifiers enum name : base { ... }``, e.g. ``base='byte'``."""

    def __init__(self, name: str, modifiers: str = 'public',
                 base: Optional[str] = None):
        super().__init__()
        self.__name = name
        self.__modifiers = modifiers
        self.__base = base
        self.__items = []

    def AddMember(self, name: str, value: Optional[object] = None) -> None:
        """Add ``name,`` or ``name = value,``."""
        self.__items.append(
            _Line(f'{name},' if value is None else f'{name} = {value},'))

    def Add(self, item: CsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = JoinWords(self.__modifiers, 'enum', self.__name,
                           f': {self.__base}' if self.__base else '')
        return self.RenderBlock(header, self.__items) + '\n'


class CsNamespace(CsItem):
    """``namespace name { ... }``. For a file-scoped namespace, use
    ``CsFile(namespace=...)`` instead."""

    def __init__(self, name: str):
        super().__init__()
        self.__name = name
        self.__items = []

    def Add(self, item: CsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        return self.RenderBlock(f'namespace {self.__name}',
                                self.__items) + '\n'
