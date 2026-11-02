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
from pysourcegen.gogen.item import GoItem


class GoSwitchCase(GoItem, SwitchCaseBase):
    """``case <case>:`` followed by the items of ``body``. Go cases do not
    fall through, so there is no ``break``."""

    def __init__(self, case: str, body):
        super().__init__(f'case {case}:', body, add_break=False)


class GoSwitchDefault(GoItem, SwitchCaseBase):
    """``default:`` followed by the items of ``body``."""

    def __init__(self, body):
        super().__init__('default:', body, add_break=False)


class GoSwitch(GoItem, SwitchBase):
    """``switch expression { ... }``, or ``switch { ... }`` when
    ``expression`` is empty. Case labels line up with ``switch``."""

    CASE_LEVEL = 0

    def __init__(self, expression: str = '', body=None):
        super().__init__(expression, body)

    def Header(self) -> str:
        return f'switch {self.expression}' if self.expression else 'switch'
