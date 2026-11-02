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

from typing import List, Optional

from pysourcegen.common import Align
from pysourcegen.gogen.item import GoItem


class _Row(GoItem):
    """A line made of cells that gofmt aligns into columns."""

    def __init__(self, cells: List[str]):
        super().__init__()
        self.cells = cells

    def __str__(self) -> str:
        return self.Indent(self.start_indent, ' '.join(self.cells))


class _AlignedBlock(GoItem):
    """A block whose rows are aligned into columns, like gofmt does.
    Other items (comments, text) are rendered as-is between the rows."""

    def __init__(self):
        super().__init__()
        self._items = []

    def Add(self, item: GoItem) -> None:
        self._items.append(item)

    def _RenderBody(self) -> str:
        level = self.start_indent + 1
        lines = []
        run = []

        def Flush():
            for line in Align([row.cells for row in run]):
                lines.append(self.Indent(level, line))
            run.clear()

        for item in self._items:
            if isinstance(item, _Row):
                run.append(item)
                continue
            Flush()
            item.SetIndent(level)
            lines.append(str(item))
        Flush()
        return '\n'.join(lines)

    def _Render(self, header: str, close: str) -> str:
        if not self._items:
            # gofmt writes an empty struct as struct{}
            return self.Indent(self.start_indent,
                               header.replace(' {', '{') + close)
        return '\n'.join([self.Indent(self.start_indent, header),
                          self._RenderBody(),
                          self.Indent(self.start_indent, close)])


class GoStruct(_AlignedBlock):
    """``type name struct { ... }``. Field names, types and tags are aligned
    into columns."""

    def __init__(self, name: str):
        super().__init__()
        self.__name = name

    def AddField(self, name: str, typename: str,
                 tag: Optional[str] = None) -> None:
        """Add ``name typename``, with ``tag`` as a struct tag, e.g.
        ``tag='json:"name"'`` gives ``name typename `json:"name"```.
        Use ``Add(GoText('io.Reader'))`` for an embedded field."""
        cells = [name, typename]
        if tag:
            cells.append(f'`{tag}`')
        self.Add(_Row(cells))

    def __str__(self) -> str:
        return self._Render(f'type {self.__name} struct {{', '}') + '\n'


class GoInterface(GoItem):
    """``type name interface { ... }``."""

    def __init__(self, name: str):
        super().__init__()
        self.__name = name
        self.__items = []

    def AddMethod(self, signature: str) -> None:
        """Add a method, e.g. ``'Read(p []byte) (n int, err error)'``."""
        self.__items.append(_Row([signature]))

    def Add(self, item: GoItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = f'type {self.__name} interface'
        if not self.__items:
            return self.Indent(self.start_indent, header + '{}') + '\n'
        return self.RenderBlock(header, self.__items) + '\n'


class GoConstBlock(_AlignedBlock):
    """A grouped declaration: ``const ( ... )``. Names, types and values are
    aligned into columns."""

    KEYWORD = 'const'

    def AddConst(self, name: str, typename: Optional[str] = None,
                 value: Optional[str] = None) -> None:
        """Add ``name [typename] [= value]``, e.g.
        ``AddConst('Red', 'Color', 'iota')`` then ``AddConst('Green')``."""
        cells = [name]
        if typename:
            cells.append(typename)
        if value is not None:
            cells.append(f'= {value}')
        self.Add(_Row(cells))

    def __str__(self) -> str:
        return self._Render(f'{self.KEYWORD} (', ')') + '\n'


class GoVarBlock(GoConstBlock):
    """A grouped declaration: ``var ( ... )``. Use ``AddVar``."""

    KEYWORD = 'var'

    def AddVar(self, name: str, typename: Optional[str] = None,
               value: Optional[str] = None) -> None:
        self.AddConst(name, typename, value)
