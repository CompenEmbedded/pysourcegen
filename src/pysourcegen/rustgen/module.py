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

from pysourcegen.rustgen.item import RsItem, Visibility


class RsMod(RsItem):
    """An inline module: ``mod name { ... }``."""

    def __init__(self, name: str, public: Union[bool, str] = False):
        super().__init__()
        self.__name = name
        self.__public = public
        self.__items = []

    def Add(self, item: RsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = f'{Visibility(self.__public)}mod {self.__name}'
        return self.RenderBlock(header, self.__items) + '\n'
