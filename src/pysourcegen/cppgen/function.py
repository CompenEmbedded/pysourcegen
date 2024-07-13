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

from pysourcegen.cppgen.item import CppItem
from pysourcegen.cppgen.body import CppBody


class CppFunction(CppItem):

    def __init__(self, name: str, return_type: str, body: CppBody):
        super().__init__([return_type + " [N]([P])", "[B]"])
        self.__name = name
        self.__returntype = return_type
        self.__parameters = []
        self.__body = body

    def AddParameter(self, typename: str, name: str) -> None:
        self.__parameters.append(f"{typename} {name}")

    def __ParseParameters(self) -> str:
        return ", ".join(self.__parameters)

    def __str__(self) -> str:
        self.__body.SetIndent(self.start_indent)
        retval = self.GetIndentedTemplate()
        retval = retval.replace('[N]', self.__name)
        retval = retval.replace('[P]', self.__ParseParameters())
        retval = retval.replace('[B]', str(self.__body))
        return retval + "\n"