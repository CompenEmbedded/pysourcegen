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

from pysourcegen.gogen.file import GoFile
from pysourcegen.gogen.function import GoFunction
from pysourcegen.gogen.item import GoBody, GoComment, GoText
from pysourcegen.gogen.switch import GoSwitch, GoSwitchCase, GoSwitchDefault
from pysourcegen.gogen.types import (GoConstBlock, GoInterface, GoStruct,
                                     GoVarBlock)

__all__ = [
    'GoBody', 'GoComment', 'GoConstBlock', 'GoFile', 'GoFunction',
    'GoInterface', 'GoStruct', 'GoSwitch', 'GoSwitchCase', 'GoSwitchDefault',
    'GoText', 'GoVarBlock'
]
