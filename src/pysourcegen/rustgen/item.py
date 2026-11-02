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

from pysourcegen.common import BlockItem


def Visibility(public: Union[bool, str]) -> str:
    """Return the visibility prefix: ``True`` gives ``'pub '``, a string such
    as ``'pub(crate)'`` is used as-is, ``False`` gives no prefix."""
    if public is True:
        return 'pub '
    if public:
        return f'{public} '
    return ''


class RsItem(BlockItem):
    """Base class for Rust items."""
