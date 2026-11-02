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

"""Output snapshot tests. Run with: python3 -m unittest discover -s tests"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pysourcegen import *  # noqa: E402,F403


class TestItems(unittest.TestCase):

    def test_empty_text_is_blank_line(self):
        self.assertEqual(str(CBody([CText('')])), '{\n\n}')
        self.assertEqual(str(CppBody([CppText('')])), '{\n\n}')

    def test_text_starting_with_bracket_is_indented(self):
        self.assertEqual(str(CppBody([CppText('[[nodiscard]] int f();')])),
                         '{\n    [[nodiscard]] int f();\n}')

    def test_empty_comment_has_no_trailing_space(self):
        self.assertEqual(str(CComment('')), '//')
        self.assertEqual(str(CppDoxyComment('')), '//!')

    def test_c_enum_is_not_enum_class(self):
        e = CEnum('Color')
        e.AddEnum('RED', 0)
        self.assertEqual(str(e), 'enum Color {\n    RED = 0,\n};\n')

    def test_cpp_enum_is_enum_class(self):
        e = CppEnum('Color')
        e.AddEnum('RED', 0)
        self.assertEqual(str(e), 'enum class Color {\n    RED = 0,\n};\n')

    def test_function(self):
        f = CFunction('main', 'int', CBody([CText('return 0;')]))
        f.AddParameter('int', 'argc')
        f.AddParameter('char**', 'argv')
        self.assertEqual(str(f),
                         'int main(int argc, char** argv)\n{\n    return 0;\n}\n')

    def test_switch(self):
        sw = CSwitch('x', CBody([
            CSwitchCase('1', CBody([CText('f();')])),
            CSwitchDefault(CBody([])),
        ]))
        self.assertEqual(str(sw), '\n'.join([
            'switch (x)',
            '{',
            '    case 1:',
            '    {',
            '        f();',
            '    }',
            '    break;',
            '    default:',
            '    {',
            '',
            '    }',
            '    break;',
            '}',
        ]))


class TestCppClass(unittest.TestCase):

    EXPECTED = '\n'.join([
        'namespace ns {',
        '    class Foo: public Base {',
        '        public:',
        '            int arr[H];',
        '    };',
        '}  // namespace ns',
    ])

    def test_class_in_namespace_items_added_first(self):
        c = CppClass('Foo')
        c.SetInheritance('Base', True)
        c.AddPublicItem(CppText('int arr[H];'))
        ns = CppNamespace('ns')
        ns.Add(c)
        self.assertEqual(str(ns), self.EXPECTED)

    def test_class_in_namespace_items_added_last(self):
        c = CppClass('Foo')
        c.SetInheritance('Base', True)
        ns = CppNamespace('ns')
        ns.Add(c)
        c.AddPublicItem(CppText('int arr[H];'))
        self.assertEqual(str(ns), self.EXPECTED)

    def test_nested_namespace_not_indented(self):
        outer = CppNamespace('a')
        inner = CppNamespace('b')
        outer.Add(inner)
        inner.Add(CppText('int x;'))
        self.assertEqual(str(outer), '\n'.join([
            'namespace a {',
            'namespace b {',
            '    int x;',
            '}  // namespace b',
            '}  // namespace a',
        ]))


class TestFiles(unittest.TestCase):

    def test_file_sections(self):
        for File, Comment, Text in ((CFile, CComment, CText),
                                    (CppFile, CppComment, CppText)):
            f = File()
            f.AddHead(Comment('head'))
            f.AddInclude('stdio.h')
            f.AddInclude('local.h', system=False)
            f.Add(Text('int x;'))
            self.assertEqual(str(f), '// head\n\n#include <stdio.h>\n'
                             '#include "local.h"\n\nint x;\n')

    def test_empty_sections_are_skipped(self):
        f = CFile()
        f.Add(CText('int x;'))
        self.assertEqual(str(f), 'int x;\n')

    def test_header_guard_used_as_is(self):
        for Header, Text in ((CHeader, CText), (CppHeader, CppText)):
            h = Header('FOO_H')
            h.Add(Text('int x;'))
            self.assertEqual(str(h), '#ifndef FOO_H\n#define FOO_H\n\n'
                             'int x;\n\n#endif  // FOO_H\n')

    def test_head_placeholder_text_is_not_replaced(self):
        f = CppFile()
        f.AddHead(CppComment('[INC] [ITEMS]'))
        self.assertEqual(str(f), '// [INC] [ITEMS]\n')


class TestRust(unittest.TestCase):

    def test_function(self):
        f = RsFunction('add', 'i32', RsBody([RsText('a + b')]), public=True)
        f.AddParameter('a', 'i32')
        f.AddParameter('b', 'i32')
        self.assertEqual(str(f),
                         'pub fn add(a: i32, b: i32) -> i32 {\n    a + b\n}\n')

    def test_function_without_return_type_and_empty_body(self):
        f = RsFunction('run', None, RsBody([]))
        f.AddParameter('&mut self')
        self.assertEqual(str(f), 'fn run(&mut self) {}\n')

    def test_comments_and_attribute(self):
        self.assertEqual(str(RsComment('')), '//')
        self.assertEqual(str(RsDocComment('Doc')), '/// Doc')
        self.assertEqual(str(RsInnerDocComment('Crate')), '//! Crate')
        self.assertEqual(str(RsAttribute('derive(Debug)')), '#[derive(Debug)]')

    def test_text_is_not_treated_as_placeholder(self):
        self.assertEqual(str(RsBody([RsText('[N]'), RsText('')])),
                         '{\n    [N]\n\n}')

    def test_enum(self):
        e = RsEnum('Color', public=True)
        e.AddVariant('Red', 0)
        e.AddVariant('Write(String)')
        self.assertEqual(str(e), 'pub enum Color {\n    Red = 0,\n'
                         '    Write(String),\n}\n')

    def test_struct_visibility(self):
        s = RsStruct('Point', public='pub(crate)')
        s.AddField('x', 'i32', public=True)
        s.AddField('y', 'i32')
        self.assertEqual(str(s), 'pub(crate) struct Point {\n'
                         '    pub x: i32,\n    y: i32,\n}\n')

    def test_impl_trait_with_match(self):
        m = RsMatch('self')
        m.AddArm('Color::Red', '"red"')
        m.AddArm('_', RsBody([RsText('"other"')]))
        fn = RsFunction('name', '&str', RsBody([m]))
        fn.AddParameter('&self')
        im = RsImpl('Color', 'Named')
        im.Add(fn)
        im.Add(RsFunction('new', 'Self', RsBody([RsText('Color::Red')])))
        self.assertEqual(str(im), '\n'.join([
            'impl Named for Color {',
            '    fn name(&self) -> &str {',
            '        match self {',
            '            Color::Red => "red",',
            '            _ => {',
            '                "other"',
            '            }',
            '        }',
            '    }',
            '',
            '    fn new() -> Self {',
            '        Color::Red',
            '    }',
            '}',
            '',
        ]))

    def test_generic_impl(self):
        im = RsImpl('Wrapper<T>', generics='T: Clone')
        self.assertEqual(str(im), 'impl<T: Clone> Wrapper<T> {}\n')
        im = RsImpl("Wrapper<'a, T>", 'fmt::Display',
                    generics="'a, T: fmt::Display")
        im.Add(RsText('// ...'))
        self.assertEqual(str(im), "impl<'a, T: fmt::Display> fmt::Display "
                         "for Wrapper<'a, T> {\n    // ...\n}\n")

    def test_match_with_semicolon(self):
        m = RsMatch('x', semicolon=True)
        m.AddArm('_', '()')
        self.assertEqual(str(m), 'match x {\n    _ => (),\n};')

    def test_mod_items_added_after_nesting(self):
        outer = RsMod('a', public=True)
        inner = RsMod('b')
        outer.Add(inner)
        inner.Add(RsText('const X: u8 = 1;'))
        self.assertEqual(str(outer), 'pub mod a {\n    mod b {\n'
                         '        const X: u8 = 1;\n    }\n}\n')

    def test_file_sections(self):
        f = RsFile()
        f.AddHead(RsComment('head'))
        f.AddAttribute('no_std')
        f.AddUse('core::fmt')
        f.Add(RsFunction('f', None, RsBody([])))
        f.Add(RsFunction('g', None, RsBody([])))
        self.assertEqual(str(f), '// head\n\n#![no_std]\n\nuse core::fmt;\n\n'
                         'fn f() {}\n\nfn g() {}\n')

    def test_empty_file_sections_are_skipped(self):
        f = RsFile()
        f.Add(RsText('const X: u8 = 1;'))
        self.assertEqual(str(f), 'const X: u8 = 1;\n')


class TestCAndCppItems(unittest.TestCase):

    def test_body_add_and_semicolon(self):
        for Body, Text in ((CBody, CText), (CppBody, CppText)):
            b = Body([], semicolon=True)
            b.Add(Text('x;'))
            self.assertEqual(str(b), '{\n    x;\n};')

    def test_doxy_comment(self):
        self.assertEqual(str(CDoxyComment('doc')), '//! doc')
        self.assertEqual(str(CppDoxyComment('doc')), '//! doc')

    def test_enum_add_item(self):
        for Enum, Comment, keyword in ((CEnum, CComment, 'enum'),
                                       (CppEnum, CppComment, 'enum class')):
            e = Enum('E')
            e.Add(Comment('first'))
            e.AddEnum('A', 1)
            self.assertEqual(str(e),
                             f'{keyword} E {{\n    // first\n    A = 1,\n}};\n')

    def test_variable_is_followed_by_blank_line(self):
        self.assertEqual(str(CVariable('int x;')), 'int x;\n')
        self.assertEqual(str(CppVariable('int x;')), 'int x;\n')

    def test_header_head_and_includes(self):
        for Header, Comment in ((CHeader, CComment), (CppHeader, CppComment)):
            h = Header('X_H')
            h.AddHead(Comment('head'))
            h.AddInclude('a.h', system=False)
            self.assertEqual(str(h), '// head\n\n#ifndef X_H\n#define X_H\n\n'
                             '#include "a.h"\n\n#endif  // X_H\n')

    def test_cpp_function_and_switch(self):
        sw = CppSwitch('x', CppBody([
            CppSwitchCase('1', CppBody([CppText('f();')])),
            CppSwitchDefault(CppBody([])),
        ]))
        f = CppFunction('g', 'void', CppBody([sw]))
        f.AddParameter('int', 'x')
        self.assertEqual(str(f), '\n'.join([
            'void g(int x)',
            '{',
            '    switch (x)',
            '    {',
            '        case 1:',
            '        {',
            '            f();',
            '        }',
            '        break;',
            '        default:',
            '        {',
            '',
            '        }',
            '        break;',
            '    }',
            '}',
            '',
        ]))

    def test_cpp_class_private_items_and_constructor(self):
        ctor = CppClassConstructor('Foo', CppBody([CppText('x_ = x;')]))
        ctor.AddParameter('int', 'x')
        c = CppClass('Foo')
        c.SetInheritance('Base', False)
        c.AddPublicItem(ctor)
        c.AddPrivateItem(CppText('int x_;'))
        self.assertEqual(str(c), '\n'.join([
            'class Foo: private Base {',
            '    public:',
            '        Foo(int x)',
            '        {',
            '            x_ = x;',
            '        }',
            '',
            '    private:',
            '        int x_;',
            '};',
        ]))


    def test_cpp_class_only_private_items(self):
        c = CppClass('Foo')
        c.AddPrivateItem(CppText('int x_;'))
        self.assertEqual(str(c),
                         'class Foo {\n    private:\n        int x_;\n};')

    def test_switch_without_cases(self):
        self.assertEqual(str(GoSwitch('x')), 'switch x {\n}')
        self.assertEqual(str(JsSwitch('x')), 'switch (x) {\n}')
        self.assertEqual(str(CsSwitch('x')), 'switch (x)\n{\n}')


class TestRustExtra(unittest.TestCase):

    def test_body_add_and_semicolon(self):
        b = RsBody([], semicolon=True)
        b.Add(RsText('x'))
        self.assertEqual(str(b), '{\n    x\n};')
        self.assertEqual(str(RsBody([])), '{}')

    def test_enum_and_struct_add_items(self):
        e = RsEnum('E')
        e.Add(RsDocComment('A'))
        e.AddVariant('A')
        self.assertEqual(str(e), 'enum E {\n    /// A\n    A,\n}\n')
        s = RsStruct('S')
        s.Add(RsDocComment('x'))
        s.AddField('x', 'u8')
        self.assertEqual(str(s), 'struct S {\n    /// x\n    x: u8,\n}\n')

    def test_match_add_arm_item(self):
        m = RsMatch('x')
        m.Add(RsComment('only'))
        m.Add(RsMatchArm('_', '0'))
        self.assertEqual(str(m), 'match x {\n    // only\n    _ => 0,\n}')


if __name__ == '__main__':
    unittest.main()
