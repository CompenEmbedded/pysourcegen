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

from pysourcegen.common import BlockItem, BodyBase, LineCommentBase, TextBase


class CsItem(BlockItem):
    """Base class for C# items. Braces go on their own line, as in the .NET
    coding conventions."""

    BRACE_ON_OWN_LINE = True


class CsText(CsItem, TextBase):
    """A line of code, copied as-is."""


class CsComment(CsItem, LineCommentBase):
    """A ``// text`` comment."""


class CsDocComment(CsItem, LineCommentBase):
    """A ``/// text`` XML doc comment. Text with newlines becomes one line
    per line, e.g. ``CsDocComment('<summary>\\nAdds.\\n</summary>')``."""

    PREFIX = '///'


class CsAttribute(CsItem, TextBase):
    """An attribute: ``CsAttribute('Serializable')`` gives
    ``[Serializable]``."""

    def __init__(self, text: str):
        super().__init__(f'[{text}]')


class CsBody(CsItem, BodyBase):
    """A ``{ ... }`` block."""
