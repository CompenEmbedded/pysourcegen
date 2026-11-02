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

from pysourcegen.rustgen.item import RsItem


class RsImpl(RsItem):
    """An ``impl`` block: ``impl Type { ... }``, or
    ``impl Trait for Type { ... }`` when ``trait`` is given.

    ``generics`` declares the impl's type parameters, e.g.
    ``RsImpl('Wrapper<T>', generics='T: Clone')`` gives
    ``impl<T: Clone> Wrapper<T> { ... }``.
    """

    def __init__(self, typename: str, trait: Optional[str] = None,
                 generics: Optional[str] = None):
        super().__init__()
        self.__typename = typename
        self.__trait = trait
        self.__generics = generics
        self.__items = []

    def Add(self, item: RsItem) -> None:
        self.__items.append(item)

    def __str__(self) -> str:
        header = f'impl<{self.__generics}>' if self.__generics else 'impl'
        if self.__trait:
            header += f' {self.__trait} for {self.__typename}'
        else:
            header += f' {self.__typename}'
        return self.RenderBlock(header, self.__items) + '\n'
