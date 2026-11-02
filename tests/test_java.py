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

"""Output tests for the Java generator (pysourcegen.javagen)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pysourcegen import *  # noqa: E402,F403


class TestJava(unittest.TestCase):

    def test_comments_and_annotation(self):
        self.assertEqual(str(JavaComment('x')), '// x')
        self.assertEqual(str(JavaDocComment('Doc')), '/** Doc */')
        self.assertEqual(str(JavaAnnotation('Override')), '@Override')

    def test_method(self):
        m = JavaMethod('main', 'void', JavaBody([JavaText('run();')]),
                       modifiers='public static', throws=['IOException',
                                                          'Exception'])
        m.AddParameter('String[]', 'args')
        self.assertEqual(str(m), 'public static void main(String[] args) '
                         'throws IOException, Exception {\n'
                         '    run();\n}\n')

    def test_constructor_and_abstract_method(self):
        c = JavaMethod('Point', None, JavaBody([]), throws='Exception')
        self.assertEqual(str(c), 'public Point() throws Exception {}\n')
        a = JavaMethod('area', 'double', None, modifiers='abstract')
        self.assertEqual(str(a), 'abstract double area();')

    def test_class(self):
        c = JavaClass('Square', modifiers='final', extends='Base',
                      implements=['Shape', 'Comparable<Square>'])
        c.AddField('double', 'side')
        c.AddField('int', 'COUNT', '0', modifiers='static')
        c.Add(JavaAnnotation('Override'))
        c.Add(JavaMethod('area', 'double',
                         JavaBody([JavaText('return side * side;')])))
        self.assertEqual(str(c), '\n'.join([
            'final class Square extends Base implements Shape, '
            'Comparable<Square> {',
            '    private double side;',
            '    static int COUNT = 0;',
            '    @Override',
            '    public double area() {',
            '        return side * side;',
            '    }',
            '}',
            '',
        ]))

    def test_interface(self):
        i = JavaInterface('Shape', extends=['A', 'B'])
        i.Add(JavaMethod('area', 'double', None, modifiers=''))
        self.assertEqual(str(i), 'public interface Shape extends A, B {\n'
                         '    double area();\n}\n')
        self.assertEqual(str(JavaInterface('I', modifiers='')),
                         'interface I {}\n')

    def test_enum_with_members(self):
        e = JavaEnum('Color')
        e.AddConstant('RED', '"red"')
        e.AddConstant('GREEN', '"green"')
        e.AddField('String', 'label', modifiers='private final')
        self.assertEqual(str(e), '\n'.join([
            'public enum Color {',
            '    RED("red"),',
            '    GREEN("green");',
            '',
            '    private final String label;',
            '}',
            '',
        ]))

    def test_enum_constants_only_and_empty(self):
        e = JavaEnum('Size', modifiers='')
        e.AddConstant('S')
        e.AddConstant('M')
        self.assertEqual(str(e), 'enum Size {\n    S,\n    M,\n}\n')
        self.assertEqual(str(JavaEnum('E')), 'public enum E {}\n')

    def test_switch(self):
        sw = JavaSwitch('c', JavaBody([
            JavaSwitchCase('RED', [JavaText('return 1;')], add_break=False),
        ]))
        sw.Add(JavaSwitchDefault(JavaBody([JavaText('n++;')])))
        self.assertEqual(str(sw), '\n'.join([
            'switch (c) {',
            '    case RED:',
            '        return 1;',
            '    default:',
            '        n++;',
            '        break;',
            '}',
        ]))

    def test_file(self):
        f = JavaFile('com.example')
        f.AddHead(JavaComment('head'))
        f.AddImport('java.util.List')
        f.AddImport('java.lang.Math.max', static=True)
        f.Add(JavaClass('Main'))
        self.assertEqual(str(f), '// head\n\npackage com.example;\n\n'
                         'import java.util.List;\n'
                         'import static java.lang.Math.max;\n\n'
                         'public class Main {}\n')
        self.assertEqual(str(JavaFile()), '\n')


if __name__ == '__main__':
    unittest.main()
