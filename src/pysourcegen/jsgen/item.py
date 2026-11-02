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

from pysourcegen.common import (BlockDocCommentBase, BlockItem, BodyBase,
                                LineCommentBase, TextBase)


def Export(export: Union[bool, str]) -> str:
    """``True`` gives ``'export'``, ``'default'`` gives ``'export default'``."""
    if export == 'default':
        return 'export default'
    return 'export' if export else ''


def Typed(name: str, typename: Optional[str]) -> str:
    """``name: typename``, or just ``name`` when there is no type."""
    return f'{name}: {typename}' if typename else name


class JsItem(BlockItem):
    """Base class for JavaScript/TypeScript items. Indented with two spaces,
    as Prettier does."""

    INDENT = '  '


class JsText(JsItem, TextBase):
    """A line of code, copied as-is."""


class JsComment(JsItem, LineCommentBase):
    """A ``// text`` comment."""


class JsDocComment(JsItem, BlockDocCommentBase):
    """A ``/** text */`` JSDoc comment. Text with newlines becomes a
    multi-line comment."""


class JsBody(JsItem, BodyBase):
    """A ``{ ... }`` block."""
