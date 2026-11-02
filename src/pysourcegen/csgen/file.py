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
from pysourcegen.csgen.item import CsItem


class CsFile:
    """A C# source file: head comments, ``using`` directives, an optional
    file-scoped namespace (``namespace name;``), then items."""

    def __init__(self, namespace: Optional[str] = None):
        self.__namespace = namespace
        self.__head = []
        self.__usings = []
        self.__items = []

    def AddHead(self, head: CsItem) -> None:
        self.__head.append(head)

    def AddUsing(self, name: str, static: bool = False) -> None:
        """Add ``using name;``, or ``using static name;``."""
        self.__usings.append(f'using {"static " if static else ""}{name};')

    def Add(self, item: CsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        return JoinSections([
            '\n'.join(str(item) for item in self.__head),
            '\n'.join(self.__usings),
            f'namespace {self.__namespace};' if self.__namespace else '',
            '\n'.join(str(item) for item in self.__items).rstrip('\n'),
        ])
