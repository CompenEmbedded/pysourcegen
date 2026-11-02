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

from pysourcegen.rustgen.item import RsItem


class RsFile:
    """A Rust source file: head comments, inner attributes, ``use``
    declarations, then items."""

    def __init__(self):
        self.__head = []
        self.__attributes = []
        self.__uses = []
        self.__items = []

    def AddHead(self, head: RsItem) -> None:
        self.__head.append(head)

    def AddAttribute(self, attribute: str) -> None:
        """Add an inner attribute: ``#![attribute]``, e.g. ``'no_std'``."""
        self.__attributes.append(f'#![{attribute}]')

    def AddUse(self, path: str) -> None:
        """Add ``use path;``, e.g. ``'std::collections::HashMap'``."""
        self.__uses.append(f'use {path};')

    def Add(self, item: RsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        sections = [
            '\n'.join(str(item) for item in self.__head),
            '\n'.join(self.__attributes),
            '\n'.join(self.__uses),
            '\n'.join(str(item) for item in self.__items).rstrip('\n'),
        ]
        # Empty sections are left out, so there are no stray blank lines
        return '\n\n'.join(s for s in sections if s) + '\n'
