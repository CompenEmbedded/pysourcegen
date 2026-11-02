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
from pysourcegen.javagen.item import JavaItem


class JavaFile:
    """A Java source file: head comments, the package declaration, imports,
    then items."""

    def __init__(self, package: Optional[str] = None):
        self.__package = package
        self.__head = []
        self.__imports = []
        self.__items = []

    def AddHead(self, head: JavaItem) -> None:
        self.__head.append(head)

    def AddImport(self, name: str, static: bool = False) -> None:
        """Add ``import name;``, or ``import static name;``."""
        self.__imports.append(f'import {"static " if static else ""}{name};')

    def Add(self, item: JavaItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        return JoinSections([
            '\n'.join(str(item) for item in self.__head),
            f'package {self.__package};' if self.__package else '',
            '\n'.join(self.__imports),
            '\n'.join(str(item) for item in self.__items).rstrip('\n'),
        ])
