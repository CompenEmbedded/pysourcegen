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

"""Output tests for the C# generator (pysourcegen.csgen)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pysourcegen import *  # noqa: E402,F403


class TestCs(unittest.TestCase):

    def test_comments_and_attribute(self):
        self.assertEqual(str(CsComment('x')), '// x')
        self.assertEqual(str(CsDocComment('<summary>\nAdds.\n</summary>')),
                         '/// <summary>\n/// Adds.\n/// </summary>')
        self.assertEqual(str(CsAttribute('Serializable')), '[Serializable]')

    def test_braces_on_own_line(self):
        self.assertEqual(str(CsBody([])), '{\n}')
        b = CsBody([CsText('x();')], semicolon=True)
        self.assertEqual(str(b), '{\n    x();\n};')

    def test_method(self):
        m = CsMethod('Add', 'int', CsBody([CsText('return a + b;')]),
                     modifiers='public static')
        m.AddParameter('int', 'a')
        m.AddParameter('int', 'b', '1')
        self.assertEqual(str(m), 'public static int Add(int a, int b = 1)\n'
                         '{\n    return a + b;\n}\n')

    def test_constructor_and_abstract_method(self):
        self.assertEqual(str(CsMethod('Point', None, CsBody([]))),
                         'public Point()\n{\n}\n')
        self.assertEqual(str(CsMethod('Area', 'double', None, modifiers='')),
                         'double Area();')

    def test_class_fields_and_properties(self):
        c = CsClass('Square', bases=['Base', 'IShape'])
        c.Add(CsAttribute('Obsolete'))
        c.AddField('double', '_side', modifiers='private readonly')
        c.AddField('int', 'Count', '0', modifiers='public static')
        c.AddProperty('string', 'Name', value='"square"')
        c.AddProperty('int', 'Sides', 'get;')
        self.assertEqual(str(c), '\n'.join([
            'public class Square : Base, IShape',
            '{',
            '    [Obsolete]',
            '    private readonly double _side;',
            '    public static int Count = 0;',
            '    public string Name { get; set; } = "square";',
            '    public int Sides { get; }',
            '}',
            '',
        ]))

    def test_struct_and_interface(self):
        self.assertEqual(str(CsStruct('P', bases='IComparable')),
                         'public struct P : IComparable\n{\n}\n')
        i = CsInterface('IShape', modifiers='internal')
        i.Add(CsMethod('Area', 'double', None, modifiers=''))
        self.assertEqual(str(i), 'internal interface IShape\n{\n'
                         '    double Area();\n}\n')

    def test_enum(self):
        e = CsEnum('Color', base='byte')
        e.Add(CsComment('first'))
        e.AddMember('Red', 1)
        e.AddMember('Green')
        self.assertEqual(str(e), 'public enum Color : byte\n{\n'
                         '    // first\n    Red = 1,\n    Green,\n}\n')
        self.assertEqual(str(CsEnum('E')), 'public enum E\n{\n}\n')

    def test_namespace(self):
        ns = CsNamespace('Outer')
        ns.Add(CsClass('A'))
        ns.Add(CsClass('B'))
        self.assertEqual(str(ns), '\n'.join([
            'namespace Outer',
            '{',
            '    public class A',
            '    {',
            '    }',
            '',
            '    public class B',
            '    {',
            '    }',
            '}',
            '',
        ]))

    def test_switch(self):
        sw = CsSwitch('c', CsBody([
            CsSwitchCase('1', [CsText('return "one";')], add_break=False),
        ]))
        sw.Add(CsSwitchDefault([]))
        self.assertEqual(str(sw), '\n'.join([
            'switch (c)',
            '{',
            '    case 1:',
            '        return "one";',
            '    default:',
            '        break;',
            '}',
        ]))

    def test_file_with_file_scoped_namespace(self):
        f = CsFile(namespace='Demo')
        f.AddHead(CsComment('head'))
        f.AddUsing('System')
        f.AddUsing('System.Math', static=True)
        f.Add(CsClass('A'))
        self.assertEqual(str(f), '// head\n\nusing System;\n'
                         'using static System.Math;\n\nnamespace Demo;\n\n'
                         'public class A\n{\n}\n')


if __name__ == '__main__':
    unittest.main()
