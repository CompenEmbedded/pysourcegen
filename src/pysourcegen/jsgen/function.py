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

from pysourcegen.common import JoinWords
from pysourcegen.jsgen.item import Export, JsBody, JsItem, Typed


class _Callable(JsItem):

    def __init__(self, name: str, return_type: Optional[str], body: JsBody):
        super().__init__()
        self._name = name
        self._returntype = return_type
        self._body = body
        self._parameters = []

    def AddParameter(self, name: str, typename: Optional[str] = None,
                     default: Optional[str] = None) -> None:
        """Add ``name``, ``name: typename`` (TypeScript), and/or
        ``= default``."""
        param = Typed(name, typename)
        if default is not None:
            param += f' = {default}'
        self._parameters.append(param)

    def _Render(self, prefix: str) -> str:
        header = f'{prefix}({", ".join(self._parameters)})'
        if self._returntype:
            header += f': {self._returntype}'
        self._body.SetIndent(self.start_indent)
        return self._body.RenderWithHeader(header) + '\n'


class JsFunction(_Callable):
    """``function name(params) { body }``.

    ``return_type`` is a TypeScript return type; leave it empty or ``None``
    for JavaScript. ``export`` may be ``True`` or ``'default'``.
    """

    def __init__(self, name: str, return_type: Optional[str], body: JsBody,
                 export: Union[bool, str] = False, is_async: bool = False):
        super().__init__(name, return_type, body)
        self.__export = export
        self.__async = is_async

    def __str__(self) -> str:
        return self._Render(JoinWords(Export(self.__export),
                                      'async' if self.__async else '',
                                      f'function {self._name}'))


class JsMethod(_Callable):
    """A class method: ``modifiers name(params) { body }``.

    ``modifiers`` is used as-is, e.g. ``'static'``, ``'async'`` or, for
    TypeScript, ``'private'``. Use the name ``'constructor'`` for a
    constructor.
    """

    def __init__(self, name: str, return_type: Optional[str], body: JsBody,
                 modifiers: str = ''):
        super().__init__(name, return_type, body)
        self.__modifiers = modifiers

    def __str__(self) -> str:
        return self._Render(JoinWords(self.__modifiers, self._name))
