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

from pysourcegen.common import JoinSections
from pysourcegen.jsgen.item import JsItem


class JsFile:
    """A JavaScript/TypeScript module: head comments, imports, then items."""

    def __init__(self):
        self.__head = []
        self.__imports = []
        self.__items = []

    def AddHead(self, head: JsItem) -> None:
        self.__head.append(head)

    def AddImport(self, module: str, names: Optional[List[str]] = None,
                  default: Optional[str] = None) -> None:
        """Add an import. ``AddImport('fs', ['readFile'])`` gives
        ``import { readFile } from "fs";``, ``AddImport('react',
        default='React')`` gives ``import React from "react";``, and
        ``AddImport('./setup.js')`` gives ``import "./setup.js";``."""
        clause = []
        if default:
            clause.append(default)
        if names:
            clause.append('{ ' + ', '.join(names) + ' }')
        if clause:
            self.__imports.append(
                f'import {", ".join(clause)} from "{module}";')
        else:
            self.__imports.append(f'import "{module}";')

    def Add(self, item: JsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        return JoinSections([
            '\n'.join(str(item) for item in self.__head),
            '\n'.join(self.__imports),
            '\n'.join(str(item) for item in self.__items).rstrip('\n'),
        ])
