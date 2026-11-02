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

"""Output tests for the Go generator (pysourcegen.gogen)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pysourcegen import *  # noqa: E402,F403


class TestGo(unittest.TestCase):

    def test_text_comment_body(self):
        b = GoBody([GoText('x := 1'), GoComment('a\nb')])
        b.Add(GoText(''))
        self.assertEqual(str(b), '{\n\tx := 1\n\t// a\n\t// b\n\n}')

    def test_function_and_method(self):
        f = GoFunction('add', 'int', GoBody([GoText('return a + b')]))
        f.AddParameter('a', 'int')
        f.AddParameter('b', 'int')
        self.assertEqual(str(f),
                         'func add(a int, b int) int {\n\treturn a + b\n}\n')
        m = GoFunction('Reset', None, GoBody([]), receiver='p *Point')
        self.assertEqual(str(m), 'func (p *Point) Reset() {}\n')

    def test_struct_aligns_fields_and_tags(self):
        s = GoStruct('Point')
        s.AddField('X', 'int', 'json:"x"')
        s.AddField('Label', 'string')
        s.Add(GoComment('breaks the alignment run'))
        s.AddField('Z', 'float64')
        self.assertEqual(str(s), '\n'.join([
            'type Point struct {',
            '\tX     int `json:"x"`',
            '\tLabel string',
            '\t// breaks the alignment run',
            '\tZ float64',
            '}',
            '',
        ]))

    def test_tags_align_in_their_own_column(self):
        s = GoStruct('T')
        s.AddField('A', 'int', 'json:"a"')
        s.AddField('Bb', 'float64', 'json:"b"')
        self.assertEqual(str(s), 'type T struct {\n'
                         '\tA  int     `json:"a"`\n'
                         '\tBb float64 `json:"b"`\n}\n')

    def test_empty_struct_and_interface(self):
        self.assertEqual(str(GoStruct('E')), 'type E struct{}\n')
        self.assertEqual(str(GoInterface('I')), 'type I interface{}\n')

    def test_interface(self):
        i = GoInterface('Shape')
        i.Add(GoComment('Area returns the area'))
        i.AddMethod('Area() float64')
        self.assertEqual(str(i), 'type Shape interface {\n'
                         '\t// Area returns the area\n\tArea() float64\n}\n')

    def test_const_and_var_blocks(self):
        c = GoConstBlock()
        c.AddConst('Red', 'Color', 'iota')
        c.AddConst('Green')
        self.assertEqual(str(c),
                         'const (\n\tRed Color = iota\n\tGreen\n)\n')
        v = GoVarBlock()
        v.AddVar('a', value='1')
        v.AddVar('long', value='2')
        self.assertEqual(str(v), 'var (\n\ta    = 1\n\tlong = 2\n)\n')

    def test_switch_cases_line_up_with_switch(self):
        inner = GoSwitch('', [GoSwitchCase('n > 1', [GoText('f()')])])
        sw = GoSwitch('c', GoBody([
            GoSwitchCase('1, 2', GoBody([inner])),
        ]))
        sw.Add(GoSwitchDefault([]))
        f = GoFunction('g', None, GoBody([sw]))
        self.assertEqual(str(f), '\n'.join([
            'func g() {',
            '\tswitch c {',
            '\tcase 1, 2:',
            '\t\tswitch {',
            '\t\tcase n > 1:',
            '\t\t\tf()',
            '\t\t}',
            '\tdefault:',
            '\t}',
            '}',
            '',
        ]))

    def test_file_sorts_imports(self):
        f = GoFile('main')
        f.AddHead(GoComment('head'))
        f.AddImport('os')
        f.AddImport('strings', 'str')
        f.AddImport('fmt')
        f.Add(GoFunction('main', None, GoBody([])))
        self.assertEqual(str(f), '// head\n\npackage main\n\nimport (\n'
                         '\t"fmt"\n\t"os"\n\tstr "strings"\n)\n\n'
                         'func main() {}\n')

    def test_file_single_and_no_imports(self):
        f = GoFile('lib')
        self.assertEqual(str(f), 'package lib\n')
        f.AddImport('fmt')
        self.assertEqual(str(f), 'package lib\n\nimport "fmt"\n')


if __name__ == '__main__':
    unittest.main()
