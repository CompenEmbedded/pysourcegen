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

from pysourcegen.common import SwitchBase, SwitchCaseBase
from pysourcegen.csgen.item import CsItem


class CsSwitchCase(CsItem, SwitchCaseBase):
    """``case <case>:`` followed by the items of ``body`` and ``break;``.
    Pass ``add_break=False`` when the body ends in ``return`` or
    ``throw``."""

    def __init__(self, case: str, body, add_break: bool = True):
        super().__init__(f'case {case}:', body, add_break)


class CsSwitchDefault(CsItem, SwitchCaseBase):
    """``default:`` followed by the items of ``body`` and ``break;``."""

    def __init__(self, body, add_break: bool = True):
        super().__init__('default:', body, add_break)


class CsSwitch(CsItem, SwitchBase):
    """``switch (expression) { ... }``. Pass the cases as a body, or add
    them with ``Add``."""

    def __init__(self, expression: str, body=None):
        super().__init__(expression, body)
