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

from pysourcegen.cppgen.item import CppItem


class CppFile:
    """A source file: head comments, includes, then items."""

    def __init__(self):
        self.__includes = []
        self.__items = []
        self.__head = []

    def AddHead(self, head: CppItem) -> None:
        self.__head.append(head)

    def AddInclude(self, include: str, system: bool = True) -> None:
        """Add ``#include <include>``, or ``#include "include"`` if
        ``system`` is False."""
        self.__includes.append(f'<{include}>' if system else f'"{include}"')

    def Add(self, item: CppItem) -> None:
        self.__items.append(item)

    def __ParseHead(self) -> str:
        return '\n'.join(str(item) for item in self.__head)

    def __ParseIncludes(self) -> str:
        return '\n'.join(f'#include {inc}' for inc in self.__includes)

    def __ParseItems(self) -> str:
        return '\n'.join(str(item) for item in self.__items).rstrip('\n')

    @staticmethod
    def _Join(sections) -> str:
        # Empty sections are left out, so there are no stray blank lines
        return '\n\n'.join(s for s in sections if s) + '\n'

    def __str__(self) -> str:
        return self._Join([
            self.__ParseHead(),
            self.__ParseIncludes(),
            self.__ParseItems(),
        ])
