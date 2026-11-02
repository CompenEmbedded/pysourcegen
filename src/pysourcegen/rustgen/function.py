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

from typing import Optional, Union

from pysourcegen.rustgen.body import RsBody
from pysourcegen.rustgen.item import RsItem, Visibility


class RsFunction(RsItem):
    """A function: ``fn name(params) -> return_type { body }``.

    Leave ``return_type`` empty or ``None`` for functions that return ``()``.
    """

    def __init__(self, name: str, return_type: Optional[str], body: RsBody,
                 public: Union[bool, str] = False):
        super().__init__()
        self.__name = name
        self.__returntype = return_type
        self.__body = body
        self.__public = public
        self.__parameters = []

    def AddParameter(self, name: str, typename: Optional[str] = None) -> None:
        """Add ``name: typename``. Without a type the name is used as-is,
        for receivers such as ``&self`` or ``&mut self``."""
        self.__parameters.append(f'{name}: {typename}' if typename else name)

    def __str__(self) -> str:
        header = (f'{Visibility(self.__public)}fn {self.__name}'
                  f'({", ".join(self.__parameters)})')
        if self.__returntype:
            header += f' -> {self.__returntype}'
        self.__body.SetIndent(self.start_indent)
        return self.__body.RenderWithHeader(header) + '\n'
