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

from pysourcegen.gogen.item import GoBody, GoItem


class GoFunction(GoItem):
    """``func name(params) return_type { body }``.

    ``return_type`` is used as-is, e.g. ``'int'`` or ``'(int, error)'``.
    Leave it empty or ``None`` for no result. Give ``receiver`` to make a
    method, e.g. ``'p *Point'`` gives ``func (p *Point) name(...)``.
    """

    def __init__(self, name: str, return_type: Optional[str], body: GoBody,
                 receiver: Optional[str] = None):
        super().__init__()
        self.__name = name
        self.__returntype = return_type
        self.__body = body
        self.__receiver = receiver
        self.__parameters = []

    def AddParameter(self, name: str, typename: str) -> None:
        """Add ``name typename``."""
        self.__parameters.append(f'{name} {typename}')

    def __str__(self) -> str:
        header = 'func '
        if self.__receiver:
            header += f'({self.__receiver}) '
        header += f'{self.__name}({", ".join(self.__parameters)})'
        if self.__returntype:
            header += f' {self.__returntype}'
        self.__body.SetIndent(self.start_indent)
        return self.__body.RenderWithHeader(header) + '\n'
