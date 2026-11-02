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

from typing import List, Optional, Union

from pysourcegen.common import JoinWords
from pysourcegen.javagen.item import JavaBody, JavaItem


class JavaMethod(JavaItem):
    """``modifiers return_type name(params) throws ... { body }``.

    Pass ``None`` as ``return_type`` for a constructor, and ``None`` as
    ``body`` for an abstract or interface method (``...;``).
    """

    def __init__(self, name: str, return_type: Optional[str],
                 body: Optional[JavaBody], modifiers: str = 'public',
                 throws: Union[str, List[str], None] = None):
        super().__init__()
        self.__name = name
        self.__returntype = return_type
        self.__body = body
        self.__modifiers = modifiers
        self.__throws = throws if isinstance(throws, str) else \
            ', '.join(throws or [])
        self.__parameters = []

    def AddParameter(self, typename: str, name: str) -> None:
        """Add ``typename name``."""
        self.__parameters.append(f'{typename} {name}')

    def __str__(self) -> str:
        header = JoinWords(self.__modifiers, self.__returntype or '',
                           f'{self.__name}({", ".join(self.__parameters)})')
        if self.__throws:
            header += f' throws {self.__throws}'
        if self.__body is None:
            return self.Indent(self.start_indent, header + ';')
        self.__body.SetIndent(self.start_indent)
        return self.__body.RenderWithHeader(header) + '\n'
