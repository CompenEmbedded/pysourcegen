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

"""Building blocks shared by the brace-style generators (Rust, Go,
JavaScript/TypeScript, Java and C#)."""

from typing import List, Sequence


class BlockItem():
    """Base class for items. Subclasses set ``INDENT`` to the string used for
    one indent level and ``BRACE_ON_OWN_LINE`` for Allman-style braces."""

    INDENT = '    '
    BRACE_ON_OWN_LINE = False

    def __init__(self):
        self.start_indent = 0

    def Indent(self, level: int, string: str) -> str:
        if not string:
            return ''
        return self.INDENT * level + string

    def SetIndent(self, level: int) -> None:
        self.start_indent = level

    def RenderItems(self, items: Sequence['BlockItem'], level: int) -> str:
        parts = []
        for item in items:
            item.SetIndent(level)
            parts.append(str(item))
        # Items such as functions end in a blank line to separate them from
        # the next item. Drop it after the last item, before the closing brace.
        if parts and parts[-1].endswith('\n'):
            parts[-1] = parts[-1].rstrip('\n')
        return '\n'.join(parts)

    def RenderBlock(self, header: str, items: Sequence['BlockItem'],
                    close: str = '}') -> str:
        """Render ``header {``, the items one level deeper, then ``close``.

        With ``BRACE_ON_OWN_LINE`` the ``{`` goes on its own line. Otherwise
        an empty block is rendered on one line, as ``header {}``.
        """
        lines = []
        if self.BRACE_ON_OWN_LINE:
            if header:
                lines.append(self.Indent(self.start_indent, header))
            lines.append(self.Indent(self.start_indent, '{'))
        else:
            opening = f'{header} {{' if header else '{'
            if not items:
                return self.Indent(self.start_indent, opening + close)
            lines.append(self.Indent(self.start_indent, opening))
        if items:
            lines.append(self.RenderItems(items, self.start_indent + 1))
        lines.append(self.Indent(self.start_indent, close))
        return '\n'.join(lines)


class TextBase(BlockItem):
    """A line of code, copied as-is."""

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return self.Indent(self.start_indent, self.text)


class LineCommentBase(BlockItem):
    """A line comment. Text with newlines becomes one comment line per line."""

    PREFIX = '//'

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return '\n'.join(
            self.Indent(self.start_indent, f'{self.PREFIX} {line}'.rstrip())
            for line in self.text.split('\n'))


class BlockDocCommentBase(BlockItem):
    """A ``/** text */`` doc comment (JSDoc, Javadoc). Text with newlines
    becomes a multi-line comment."""

    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        lines = self.text.split('\n')
        if len(lines) == 1:
            return self.Indent(self.start_indent, f'/** {self.text} */')
        out = ['/**'] + [f' * {line}'.rstrip() for line in lines] + [' */']
        return '\n'.join(self.Indent(self.start_indent, line) for line in out)


class BodyBase(BlockItem):
    """A ``{ ... }`` block."""

    def __init__(self, body: List[BlockItem], semicolon: bool = False):
        super().__init__()
        self.items = body
        self.semicolon = semicolon

    def Add(self, item: BlockItem) -> None:
        self.items.append(item)

    def RenderWithHeader(self, header: str) -> str:
        return self.RenderBlock(header, self.items,
                                '};' if self.semicolon else '}')

    def __str__(self) -> str:
        return self.RenderWithHeader('')


def BodyItems(body) -> List[BlockItem]:
    """The items of a body object, or the list itself."""
    if isinstance(body, BodyBase):
        return body.items
    return list(body)


class SwitchCaseBase(BlockItem):
    """``label`` followed by the body items one level deeper, then
    ``break;`` if ``add_break`` is set."""

    def __init__(self, label: str, body, add_break: bool):
        super().__init__()
        self.label = label
        self.body = body
        self.add_break = add_break

    def __str__(self) -> str:
        lines = [self.Indent(self.start_indent, self.label)]
        items = BodyItems(self.body)
        if items:
            lines.append(self.RenderItems(items, self.start_indent + 1))
        if self.add_break:
            lines.append(self.Indent(self.start_indent + 1, 'break;'))
        return '\n'.join(lines)


class SwitchBase(BlockItem):
    """A switch statement. Cases are given as a body (like ``CSwitch``) or
    added with ``Add``. ``CASE_LEVEL`` is how far case labels are indented
    relative to the ``switch`` keyword: 1, or 0 for Go."""

    CASE_LEVEL = 1

    def __init__(self, expression: str, body=None):
        super().__init__()
        self.expression = expression
        self.cases = BodyItems(body) if body is not None else []

    def Add(self, case: BlockItem) -> None:
        self.cases.append(case)

    def Header(self) -> str:
        return f'switch ({self.expression})'

    def __str__(self) -> str:
        if self.BRACE_ON_OWN_LINE:
            lines = [self.Indent(self.start_indent, self.Header()),
                     self.Indent(self.start_indent, '{')]
        else:
            lines = [self.Indent(self.start_indent, self.Header() + ' {')]
        if self.cases:
            lines.append(self.RenderItems(self.cases,
                                          self.start_indent + self.CASE_LEVEL))
        lines.append(self.Indent(self.start_indent, '}'))
        return '\n'.join(lines)


def JoinWords(*words: str) -> str:
    """Join the non-empty words with single spaces."""
    return ' '.join(w for w in words if w)


def JoinSections(sections: Sequence[str]) -> str:
    """Join file sections with one blank line, leaving out empty ones."""
    return '\n\n'.join(s for s in sections if s) + '\n'


def Align(rows: List[List[str]]) -> List[str]:
    """Align cells into columns the way gofmt's tabwriter does: a column is
    padded to its widest cell plus one space, within each run of consecutive
    rows that have a cell after it."""
    widths = [[0] * len(row) for row in rows]

    def Format(lo: int, hi: int, col: int) -> None:
        i = lo
        while i < hi:
            if len(rows[i]) - 1 <= col:
                i += 1
                continue
            j = i
            while j < hi and len(rows[j]) - 1 > col:
                j += 1
            width = max(len(rows[k][col]) for k in range(i, j))
            for k in range(i, j):
                widths[k][col] = width
            Format(i, j, col + 1)
            i = j

    Format(0, len(rows), 0)
    return [''.join(cell.ljust(widths[r][c] + 1) if c < len(row) - 1 else cell
                    for c, cell in enumerate(row))
            for r, row in enumerate(rows)]
