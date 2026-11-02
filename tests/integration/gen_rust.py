#!/usr/bin/env python3

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

"""Print a Rust program that uses every class of the generator."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from pysourcegen import *  # noqa: E402,F403
f = RsFile()
f.AddHead(RsInnerDocComment('Generated crate covering every Rs class'))
f.AddAttribute('allow(dead_code)')
f.AddUse('std::fmt')

e = RsEnum('Color', public=True)
e.Add(RsDocComment('Primary colour'))
e.AddVariant('Red', 0)
e.AddVariant('Green', 1)
f.Add(RsAttribute('derive(Debug, Clone, Copy, PartialEq)'))
f.Add(e)

msg = RsEnum('Message')
msg.AddVariant('Quit')
msg.AddVariant('Move { x: i32, y: i32 }')
msg.AddVariant('Write(String)')
f.Add(msg)

s = RsStruct('Point', public='pub(crate)')
s.Add(RsDocComment('X coordinate'))
s.AddField('x', 'i32', public=True)
s.AddField('y', 'i32')
f.Add(RsAttribute('derive(Debug, Default)'))
f.Add(s)

w = RsStruct("Wrapper<'a, T>")
w.AddField('inner', "&'a T")
f.Add(w)

disp = RsImpl('Color', 'fmt::Display')
m = RsMatch('self')
m.AddArm('Color::Red', 'write!(f, "red")')
m.AddArm('Color::Green', RsBody([RsText('write!(f, "green")')]))
fn = RsFunction('fmt', 'fmt::Result', RsBody([m]))
fn.AddParameter('&self'); fn.AddParameter('f', '&mut fmt::Formatter')
disp.Add(fn)
f.Add(disp)

pimpl = RsImpl('Point')
new = RsFunction('new', 'Self', RsBody([RsText('Point { x, y }')]), public=True)
new.AddParameter('x', 'i32'); new.AddParameter('y', 'i32')
pimpl.Add(new)
reset = RsFunction('reset', None, RsBody([RsText('self.x = 0;'), RsText('self.y = 0;')]))
reset.AddParameter('&mut self')
pimpl.Add(reset)
f.Add(pimpl)

g = RsImpl("Wrapper<'a, T>", 'fmt::Display', generics="'a, T: fmt::Display")
gf = RsFunction('fmt', 'fmt::Result', RsBody([RsText('write!(f, "[{}]", self.inner)')]))
gf.AddParameter('&self'); gf.AddParameter('f', '&mut fmt::Formatter')
g.Add(gf)
f.Add(g)

f.Add(RsImpl('Color', 'Eq'))

md = RsMod('util', public=True)
inner = RsMod('consts', public='pub(crate)')
inner.Add(RsText('pub const ANSWER: u8 = 42;'))
md.Add(inner)
dbl = RsFunction('double', 'u8', RsBody([RsText('x * 2')]), public=True)
dbl.AddParameter('x', 'u8')
md.Add(RsComment('Doubles a value'))
md.Add(dbl)
f.Add(md)

desc = RsMatch('msg', semicolon=True)
desc.AddArm('Message::Quit', 'println!("quit")')
desc.AddArm('Message::Move { x, y }', 'println!("move {x} {y}")')
desc.AddArm('_', RsBody([RsComment('anything else'), RsText('println!("other");')]))
main = RsFunction('main', None, RsBody([
    RsText('let mut p = Point::new(1, 2);'),
    RsText('p.reset();'),
    RsText('println!("{:?} {} {}", p, Color::Green, Wrapper { inner: &5 });'),
    RsText('assert_eq!(util::double(util::consts::ANSWER), 84);'),
    RsText('let msg = Message::Write(String::from("hi"));'),
    desc,
    RsBody([RsText('let _block = Message::Quit;')]),
]))
f.Add(main)
print(f, end='')
