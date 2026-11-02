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

from typing import List

from pysourcegen.rustgen.item import RsItem


class RsBody(RsItem):
    """A ``{ ... }`` block. Functions and match arms put the opening brace at
    the end of their own line, as rustfmt does."""

    def __init__(self, body: List[RsItem], semicolon: bool = False):
        super().__init__()
        self.__body = body
        self.__semicolon = semicolon

    def Add(self, item: RsItem) -> None:
        self.__body.append(item)

    def RenderWithHeader(self, header: str) -> str:
        return self.RenderBlock(header, self.__body,
                                '};' if self.__semicolon else '}')

    def __str__(self) -> str:
        return self.RenderWithHeader('')
