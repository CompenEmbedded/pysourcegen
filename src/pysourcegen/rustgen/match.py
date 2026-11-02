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

from typing import Union

from pysourcegen.rustgen.body import RsBody
from pysourcegen.rustgen.item import RsItem


class RsMatchArm(RsItem):
    """A match arm. With a string body: ``pattern => body,``.
    With an ``RsBody``: ``pattern => { ... }``."""

    def __init__(self, pattern: str, body: Union[str, RsBody]):
        super().__init__()
        self.__pattern = pattern
        self.__body = body

    def __str__(self) -> str:
        if isinstance(self.__body, RsBody):
            self.__body.SetIndent(self.start_indent)
            return self.__body.RenderWithHeader(f'{self.__pattern} =>')
        return self.Indent(self.start_indent,
                           f'{self.__pattern} => {self.__body},')


class RsMatch(RsItem):
    """A ``match expression { ... }`` expression."""

    def __init__(self, expression: str, semicolon: bool = False):
        super().__init__()
        self.__expression = expression
        self.__semicolon = semicolon
        self.__arms = []

    def AddArm(self, pattern: str, body: Union[str, RsBody]) -> None:
        self.__arms.append(RsMatchArm(pattern, body))

    def Add(self, item: RsItem) -> None:
        self.__arms.append(item)

    def __str__(self) -> str:
        return self.RenderBlock(f'match {self.__expression}', self.__arms,
                                '};' if self.__semicolon else '}')
