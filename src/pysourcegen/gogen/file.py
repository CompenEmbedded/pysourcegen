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

from typing import Optional

from pysourcegen.common import JoinSections
from pysourcegen.gogen.item import GoItem


class GoFile:
    """A Go source file: head comments, the package clause, imports, then
    items. Imports are sorted, as gofmt does."""

    def __init__(self, package: str):
        self.__package = package
        self.__head = []
        self.__imports = {}
        self.__items = []

    def AddHead(self, head: GoItem) -> None:
        self.__head.append(head)

    def AddImport(self, path: str, alias: Optional[str] = None) -> None:
        """Add ``import "path"``, or ``import alias "path"``."""
        self.__imports[path] = f'{alias} "{path}"' if alias else f'"{path}"'

    def Add(self, item: GoItem) -> None:
        self.__items.append(item)

    def __ParseImports(self) -> str:
        specs = [self.__imports[path] for path in sorted(self.__imports)]
        if not specs:
            return ''
        if len(specs) == 1:
            return f'import {specs[0]}'
        return 'import (\n' + ''.join(f'\t{s}\n' for s in specs) + ')'

    def __str__(self) -> str:
        return JoinSections([
            '\n'.join(str(item) for item in self.__head),
            f'package {self.__package}',
            self.__ParseImports(),
            '\n'.join(str(item) for item in self.__items).rstrip('\n'),
        ])
