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

"""Output tests for the JavaScript/TypeScript generator (pysourcegen.jsgen)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pysourcegen import *  # noqa: E402,F403


class TestJs(unittest.TestCase):

    def test_comments(self):
        self.assertEqual(str(JsComment('x')), '// x')
        self.assertEqual(str(JsDocComment('One line')), '/** One line */')
        self.assertEqual(str(JsDocComment('Line\n\n@returns x')),
                         '/**\n * Line\n *\n * @returns x\n */')

    def test_function_javascript(self):
        f = JsFunction('add', None, JsBody([JsText('return a + b;')]))
        f.AddParameter('a')
        f.AddParameter('b', default='1')
        self.assertEqual(str(f),
                         'function add(a, b = 1) {\n  return a + b;\n}\n')

    def test_function_typescript_export_async(self):
        f = JsFunction('run', 'Promise<void>', JsBody([]), export=True,
                       is_async=True)
        f.AddParameter('n', 'number', '0')
        self.assertEqual(str(f), 'export async function run(n: number = 0)'
                         ': Promise<void> {}\n')
        d = JsFunction('main', None, JsBody([]), export='default')
        self.assertEqual(str(d), 'export default function main() {}\n')

    def test_class(self):
        c = JsClass('Square', extends='Shape', implements=['A', 'B'],
                    export=True)
        c.AddField('side', 'number')
        c.AddField('count', value='0', modifiers='static')
        ctor = JsMethod('constructor', None, JsBody([JsText('super();')]))
        c.Add(ctor)
        c.Add(JsMethod('area', 'number', JsBody([JsText('return 1;')]),
                       modifiers='static'))
        self.assertEqual(str(c), '\n'.join([
            'export class Square extends Shape implements A, B {',
            '  side: number;',
            '  static count = 0;',
            '  constructor() {',
            '    super();',
            '  }',
            '',
            '  static area(): number {',
            '    return 1;',
            '  }',
            '}',
            '',
        ]))

    def test_empty_class(self):
        self.assertEqual(str(JsClass('A')), 'class A {}\n')

    def test_interface(self):
        i = JsInterface('Shape', extends='Base', export=True)
        i.Add(JsDocComment('The name'))
        i.AddMember('name', 'string')
        i.AddMember('sides', 'number', optional=True)
        self.assertEqual(str(i), 'export interface Shape extends Base {\n'
                         '  /** The name */\n  name: string;\n'
                         '  sides?: number;\n}\n')
        self.assertEqual(str(JsInterface('I')), 'interface I {}\n')

    def test_enum(self):
        e = JsEnum('Color', export=True, const=True)
        e.Add(JsComment('first'))
        e.AddMember('Red', '"red"')
        e.AddMember('Green')
        self.assertEqual(str(e), 'export const enum Color {\n  // first\n'
                         '  Red = "red",\n  Green,\n}\n')

    def test_switch(self):
        sw = JsSwitch('n', JsBody([
            JsSwitchCase('0', JsBody([JsText('return "zero";')]),
                         add_break=False),
            JsSwitchCase('1', [JsText('n++;')]),
        ]))
        sw.Add(JsSwitchDefault([]))
        self.assertEqual(str(sw), '\n'.join([
            'switch (n) {',
            '  case 0:',
            '    return "zero";',
            '  case 1:',
            '    n++;',
            '    break;',
            '  default:',
            '    break;',
            '}',
        ]))

    def test_body_semicolon(self):
        b = JsBody([], semicolon=True)
        b.Add(JsText('a: 1,'))
        self.assertEqual(str(b), '{\n  a: 1,\n};')

    def test_file_imports(self):
        f = JsFile()
        f.AddHead(JsComment('head'))
        f.AddImport('react', ['useState'], default='React')
        f.AddImport('./setup.js')
        f.Add(JsText('export const x = 1;'))
        self.assertEqual(str(f), '// head\n\n'
                         'import React, { useState } from "react";\n'
                         'import "./setup.js";\n\nexport const x = 1;\n')


if __name__ == '__main__':
    unittest.main()
