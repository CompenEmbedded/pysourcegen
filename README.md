# pysourcegen

Python Source Code Generator

[![Tests](https://github.com/CompenEmbedded/pysourcegen/actions/workflows/test.yml/badge.svg)](https://github.com/CompenEmbedded/pysourcegen/actions/workflows/test.yml)

A different approach for generating repetitive source code using Python.
Supported languages: C, C++, Rust, Go, JavaScript/TypeScript, Java and C#.
Instead of filling in text templates, you build the source file from Python
objects (files, functions, classes, switches, ...) and print it. Indentation
and braces are handled for you.

## Installation

```sh
pip install pysourcegen
```

Requires Python 3.8 or newer. There are no runtime dependencies.

## Quick start

```python
from pysourcegen import *

f = CppFile()
f.AddHead(CppComment('This is a generated file'))
f.AddInclude('iostream')

body = CppBody([])
body.Add(CppText('std::cout << "Hello World" << std::endl;'))
body.Add(CppText('return 0;'))

main = CppFunction('main', 'int', body)
main.AddParameter('int', 'argc')
main.AddParameter('char**', 'argv')
f.Add(main)

print(f)
```

Output:

```cpp
// This is a generated file

#include <iostream>

int main(int argc, char** argv)
{
    std::cout << "Hello World" << std::endl;
    return 0;
}
```

## Examples

The examples in `src/` print a program that has 1000 "Hello World" lines.
Run them from the `src/` directory, or install the package first.

### C++ - Hello World

Run [src/hello_world_cpp_example.py](src/hello_world_cpp_example.py) to build an executable called `cpphello`:

    ./hello_world_cpp_example.py | g++ -x c++ -o cpphello -

### C - Hello World

Run [src/hello_world_c_example.py](src/hello_world_c_example.py) to build an executable called `chello`:

    ./hello_world_c_example.py | gcc -x c -o chello -

### Rust - Hello World

Run [src/hello_world_rust_example.py](src/hello_world_rust_example.py) to build an executable called `rshello`:

    ./hello_world_rust_example.py | rustc -o rshello -

## API overview

`from pysourcegen import *` gives you the classes for every language. Each
language has its own prefix:

| Language | Prefix | Section |
|----------|--------|---------|
| C | `C` | [Files](#files), [Code items](#code-items) |
| C++ | `Cpp` | [Files](#files), [Code items](#code-items), [C++ only](#c-only) |
| Rust | `Rs` | [Rust](#rust) |
| Go | `Go` | [Go](#go) |
| JavaScript / TypeScript | `Js` | [JavaScript / TypeScript](#javascript--typescript) |
| Java | `Java` | [Java](#java) |
| C# | `Cs` | [C#](#c) |

Each object turns into source code when you call `str()` on it or print it.
The C and C++ classes work the same way.

The other languages share some conventions:

- Each has a file class (`RsFile`, `GoFile`, ...) with `AddHead(item)` for
  comments at the top and `Add(item)` for the body. It also has a method for
  that language's imports.
- `...Text(text)` is a line of code copied as-is, `...Comment(text)` is a `//`
  comment, and `...Body(items)` is a `{ ... }` block.
- Text with newlines in a comment becomes one comment line per line.
- Containers have `Add(item)` for any item, such as comments, plus helpers
  such as `AddField` for their usual members.
- Switches take their cases as a body, the same as `CSwitch`, or through
  `Add(case)`. In JavaScript, Java and C#, a case ends in `break;` unless you
  pass `add_break=False`.
- The output follows each language's standard formatter: rustfmt, gofmt,
  Prettier for JavaScript/TypeScript, and the .NET conventions for C#.

### Files

| C | C++ | Description |
|---|-----|-------------|
| `CFile()` | `CppFile()` | Source file: head comments, then includes, then items. |
| `CHeader(guard_name)` | `CppHeader(guard_name)` | Header file with an include guard. `guard_name` is used as-is, e.g. `CHeader('MY_DRIVER_H')`. |

Empty sections are left out. Non-empty sections are separated by one blank line.

Methods on file and header objects:

- `AddHead(item)`: add an item (usually a comment) to the top of the file.
- `AddInclude(name, system=True)`: add `#include <name>`, or `#include "name"` when `system=False`.
- `Add(item)`: add an item to the file body.

### Code items

| C | C++ | Description |
|---|-----|-------------|
| `CBody(items, semicolon=False)` | `CppBody(items, semicolon=False)` | A `{ ... }` block. `items` is a list of items. With `semicolon=True` the block ends in `};`. Use `Add(item)` to add more items. |
| `CFunction(name, return_type, body)` | `CppFunction(name, return_type, body)` | A function definition. Use `AddParameter(type, name)` to add parameters. |
| `CText(text)` | `CppText(text)` | A line of code, copied as-is. |
| `CComment(text)` | `CppComment(text)` | A `// text` comment. |
| `CDoxyComment(text)` | `CppDoxyComment(text)` | A `//! text` Doxygen comment. |
| `CVariable(text)` | `CppVariable(text)` | A line of text followed by a blank line. |
| `CEnum(name)` | `CppEnum(name)` | `enum name { ... };` in C, `enum class name { ... };` in C++. Use `AddEnum(name, value)` for entries, or `Add(item)` for other items such as comments. |
| `CSwitch(variable, body)` | `CppSwitch(variable, body)` | A `switch (variable)` statement. `body` is a body that holds the cases. |
| `CSwitchCase(case, body)` | `CppSwitchCase(case, body)` | `case <case>:` followed by `body` and `break;`. |
| `CSwitchDefault(body)` | `CppSwitchDefault(body)` | `default:` followed by `body` and `break;`. |

### C++ only

- `CppNamespace(name)`: `namespace name { ... }  // namespace name`. Use `Add(item)` to add items. Items are indented one level. Nested namespaces are not indented.
- `CppClass(name)`: a class definition.
  - `AddPublicItem(item)` / `AddPrivateItem(item)`: add a member to the `public:` or `private:` section.
  - `SetInheritance(base, public)`: inherit from `base`, publicly if `public` is `True`, privately if not.
- `CppClassConstructor(name, body)`: a constructor. Use `AddParameter(type, name)` to add parameters.

### Rust

The Rust classes follow Rust conventions: opening braces stay on the same line,
and parameters and fields are written `name: type`. Items that take a `public`
argument accept `True` (for `pub`), `False` (private, the default), or a string
such as `'pub(crate)'`.

| Class | Description |
|-------|-------------|
| `RsFile()` | Source file: head comments, inner attributes, `use` declarations, then items. Methods: `AddHead(item)`, `AddAttribute(attr)` for `#![attr]`, `AddUse(path)` for `use path;`, `Add(item)`. |
| `RsBody(items, semicolon=False)` | A `{ ... }` block. Use `Add(item)` to add more items. |
| `RsFunction(name, return_type, body, public=False)` | `fn name(...) -> return_type { ... }`. Pass `None` as `return_type` for `()`. Use `AddParameter(name, type)` to add parameters, or `AddParameter('&self')` for a receiver. **Note:** the order is name, then type, unlike `CppFunction`. |
| `RsStruct(name, public=False)` | A struct. Use `AddField(name, type, public=False)` for fields, or `Add(item)` for other items such as doc comments. |
| `RsEnum(name, public=False)` | An enum. Use `AddVariant(name, value=None)` for `Name,` or `Name = value,`, or `Add(item)` for other items. |
| `RsImpl(type, trait=None, generics=None)` | `impl Type { ... }`, or `impl Trait for Type { ... }`. With `generics` you get `impl<generics> ...`, e.g. `RsImpl('Wrapper<T>', 'fmt::Display', generics='T: fmt::Display')` gives `impl<T: fmt::Display> fmt::Display for Wrapper<T>`. Use `Add(item)` to add functions. |
| `RsMod(name, public=False)` | An inline `mod name { ... }`. Use `Add(item)` to add items. |
| `RsMatch(expression, semicolon=False)` | `match expression { ... }`. Use `AddArm(pattern, body)` to add arms. With a string `body` you get `pattern => body,`, and with an `RsBody` you get `pattern => { ... }`. Use `'_'` as the pattern for the default arm. |
| `RsText(text)` | A line of code, copied as-is. |
| `RsComment(text)` | A `// text` comment. |
| `RsDocComment(text)` | A `/// text` doc comment. |
| `RsInnerDocComment(text)` | A `//! text` inner doc comment. |
| `RsAttribute(text)` | An outer attribute `#[text]`, e.g. `RsAttribute('derive(Debug)')`. |

```python
from pysourcegen import *

f = RsFile()
f.AddUse('std::fmt')

e = RsEnum('Color', public=True)
for i, name in enumerate(['Red', 'Green']):
    e.AddVariant(name, i)
f.Add(RsAttribute('derive(Debug, Clone, Copy)'))
f.Add(e)

m = RsMatch('self')
m.AddArm('Color::Red', 'write!(f, "red")')
m.AddArm('Color::Green', 'write!(f, "green")')
fmt = RsFunction('fmt', 'fmt::Result', RsBody([m]))
fmt.AddParameter('&self')
fmt.AddParameter('f', '&mut fmt::Formatter')

impl = RsImpl('Color', 'fmt::Display')
impl.Add(fmt)
f.Add(impl)
print(f)
```

Output:

```rust
use std::fmt;

#[derive(Debug, Clone, Copy)]
pub enum Color {
    Red = 0,
    Green = 1,
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Color::Red => write!(f, "red"),
            Color::Green => write!(f, "green"),
        }
    }
}
```

### Go

Indented with tabs. Struct fields, tags and `const`/`var` blocks are aligned
into columns, as gofmt does.

| Class | Description |
|-------|-------------|
| `GoFile(package)` | Head comments, `package`, imports, then items. `AddImport(path, alias=None)`. Imports are sorted and grouped in `import ( ... )` when there is more than one. |
| `GoFunction(name, return_type, body, receiver=None)` | `func name(...) return_type { ... }`. `return_type` may be `None`, `'int'` or `'(int, error)'`. With `receiver='p *Point'` it is a method. `AddParameter(name, type)`. |
| `GoStruct(name)` | `type name struct { ... }`. `AddField(name, type, tag=None)`, e.g. `tag='json:"x"'`. Embedded fields: `Add(GoText('io.Reader'))`. |
| `GoInterface(name)` | `type name interface { ... }`. `AddMethod('Area() float64')`. |
| `GoConstBlock()` / `GoVarBlock()` | `const ( ... )` / `var ( ... )`. `AddConst(name, type=None, value=None)` / `AddVar(...)`. |
| `GoSwitch(expression='', body=None)` | `switch expression { ... }`, or `switch { ... }`. Cases: `GoSwitchCase(case, body)`, `GoSwitchDefault(body)`. There is no `break`. |
| `GoText`, `GoComment`, `GoBody` | See the shared conventions above. |

```python
from pysourcegen import *

f = GoFile('shapes')
f.AddImport('math')

s = GoStruct('Circle')
s.AddField('Center', 'Point', 'json:"center"')
s.AddField('R', 'float64', 'json:"r"')
f.Add(s)

area = GoFunction('Area', 'float64', GoBody([GoText('return math.Pi * c.R * c.R')]),
                  receiver='c Circle')
f.Add(area)
print(f)
```

Output:

```go
package shapes

import "math"

type Circle struct {
	Center Point   `json:"center"`
	R      float64 `json:"r"`
}

func (c Circle) Area() float64 {
	return math.Pi * c.R * c.R
}
```

### JavaScript / TypeScript

One generator for both. Indented with two spaces. Type arguments are
optional: leave them out for JavaScript, give them for TypeScript.

| Class | Description |
|-------|-------------|
| `JsFile()` | Head comments, imports, then items. `AddImport(module, names=None, default=None)` gives `import x, { a, b } from "module";`, or `import "module";`. |
| `JsFunction(name, return_type, body, export=False, is_async=False)` | `function name(...) { ... }`. `export` may be `True` or `'default'`. `AddParameter(name, type=None, default=None)`. |
| `JsClass(name, extends=None, implements=None, export=False)` | A class. `AddField(name, type=None, value=None, modifiers='')`. Add methods with `Add(JsMethod(...))`. |
| `JsMethod(name, return_type, body, modifiers='')` | A class method, e.g. `modifiers='static'`. Use the name `'constructor'` for a constructor. |
| `JsInterface(name, extends=None, export=False)` | TypeScript only. `AddMember(name, type, optional=False)`. |
| `JsEnum(name, export=False, const=False)` | TypeScript only. `AddMember(name, value=None)`. |
| `JsSwitch(expression, body=None)` | Cases: `JsSwitchCase(case, body, add_break=True)`, `JsSwitchDefault(body, add_break=True)`. |
| `JsText`, `JsComment`, `JsDocComment`, `JsBody` | `JsDocComment` is a `/** ... */` JSDoc comment. |

```python
from pysourcegen import *

f = JsFile()
i = JsInterface('Shape', export=True)
i.AddMember('name', 'string')
i.AddMember('area()', 'number')
f.Add(i)

fn = JsFunction('describe', 'string', JsBody([
    JsText('return `${shape.name}: ${shape.area()}`;'),
]), export=True)
fn.AddParameter('shape', 'Shape')
f.Add(fn)
print(f)
```

Output:

```ts
export interface Shape {
  name: string;
  area(): number;
}

export function describe(shape: Shape): string {
  return `${shape.name}: ${shape.area()}`;
}
```

### Java

Parameters and fields take the type first, the same as in C/C++.

| Class | Description |
|-------|-------------|
| `JavaFile(package=None)` | Head comments, `package`, imports, then items. `AddImport(name, static=False)`. |
| `JavaClass(name, modifiers='public', extends=None, implements=None)` | A class. `AddField(type, name, value=None, modifiers='private')`. Add methods with `Add(JavaMethod(...))`. |
| `JavaInterface(name, modifiers='public', extends=None)` | An interface. |
| `JavaEnum(name, modifiers='public')` | `AddConstant(name, args=None)`. Fields and methods added with `AddField`/`Add` come after the constants. |
| `JavaMethod(name, return_type, body, modifiers='public', throws=None)` | `return_type=None` makes a constructor, and `body=None` an abstract method. `AddParameter(type, name)`. |
| `JavaSwitch(expression, body=None)` | Cases: `JavaSwitchCase(case, body, add_break=True)`, `JavaSwitchDefault(body, add_break=True)`. |
| `JavaText`, `JavaComment`, `JavaDocComment`, `JavaAnnotation`, `JavaBody` | `JavaDocComment` is a `/** ... */` Javadoc comment. `JavaAnnotation('Override')` gives `@Override`. |

```python
from pysourcegen import *

f = JavaFile('com.example')
c = JavaClass('Circle', implements='Shape')
c.AddField('double', 'r', modifiers='private final')
ctor = JavaMethod('Circle', None, JavaBody([JavaText('this.r = r;')]))
ctor.AddParameter('double', 'r')
c.Add(ctor)
c.Add(JavaAnnotation('Override'))
c.Add(JavaMethod('area', 'double', JavaBody([JavaText('return Math.PI * r * r;')])))
f.Add(c)
print(f)
```

Output:

```java
package com.example;

public class Circle implements Shape {
    private final double r;
    public Circle(double r) {
        this.r = r;
    }

    @Override
    public double area() {
        return Math.PI * r * r;
    }
}
```

### C#

Braces go on their own line, following the .NET conventions. Parameters and
fields take the type first.

| Class | Description |
|-------|-------------|
| `CsFile(namespace=None)` | Head comments, `using` directives, an optional file-scoped `namespace name;`, then items. `AddUsing(name, static=False)`. |
| `CsNamespace(name)` | A `namespace name { ... }` block. |
| `CsClass(name, modifiers='public', bases=None)` | A class. `bases` is a name or a list of names. `AddField(type, name, value=None, modifiers='private')`, `AddProperty(type, name, accessors='get; set;', value=None, modifiers='public')`. |
| `CsStruct(...)` / `CsInterface(...)` | Same arguments as `CsClass`. |
| `CsEnum(name, modifiers='public', base=None)` | `AddMember(name, value=None)`. |
| `CsMethod(name, return_type, body, modifiers='public')` | `return_type=None` makes a constructor, and `body=None` an abstract method. `AddParameter(type, name, default=None)`. |
| `CsSwitch(expression, body=None)` | Cases: `CsSwitchCase(case, body, add_break=True)`, `CsSwitchDefault(body, add_break=True)`. |
| `CsText`, `CsComment`, `CsDocComment`, `CsAttribute`, `CsBody` | `CsDocComment` is a `///` XML doc comment. `CsAttribute('Serializable')` gives `[Serializable]`. |

```python
from pysourcegen import *

f = CsFile(namespace='Shapes')
f.AddUsing('System')
c = CsClass('Circle', bases='IShape')
c.AddProperty('double', 'R', 'get;')
m = CsMethod('Area', 'double', CsBody([CsText('return Math.PI * R * R;')]))
c.Add(m)
f.Add(c)
print(f)
```

Output:

```csharp
using System;

namespace Shapes;

public class Circle : IShape
{
    public double R { get; }
    public double Area()
    {
        return Math.PI * R * R;
    }
}
```

### Switch example

```python
from pysourcegen import *

cases = CppBody([])
for i, name in enumerate(['zero', 'one', 'two']):
    cases.Add(CppSwitchCase(str(i), CppBody([CppText(f'return "{name}";')])))
cases.Add(CppSwitchDefault(CppBody([CppText('return "unknown";')])))

fn = CppFunction('ToString', 'const char*', CppBody([CppSwitch('value', cases)]))
fn.AddParameter('int', 'value')
print(fn)
```

## Running the tests

The unit tests check the exact output of every class:

```sh
python3 -m unittest discover -s tests
```

The Docker image in [docker/](docker/Dockerfile) has the compilers for every
supported language. It runs the unit tests with branch coverage and fails if
coverage is below 100%. Then it generates a program in every language and
compiles it, runs it and checks it with the language's formatter (rustfmt,
gofmt, `tsc --strict`, `javac -Werror`, `dotnet format`, ...):

```sh
docker build -t pysourcegen-test docker/
docker run --rm -v "$PWD:/src:ro" pysourcegen-test
```

GitHub Actions runs the same container on every push and pull request.

## Changelog

### 0.0.4

- Added a Rust source generator (`RsFile`, `RsFunction`, `RsStruct`, `RsEnum`,
  `RsImpl`, `RsMod`, `RsMatch`, ...). See [Rust](#rust).
- `RsImpl` takes `generics` for generic impls such as `impl<T: Clone> Wrapper<T>`.
- Added Go (`Go...`), JavaScript/TypeScript (`Js...`), Java (`Java...`) and C#
  (`Cs...`) source generators.
- **Breaking:** `CHeader` now uses its guard name as given, the same as
  `CppHeader`. To keep the old guard, pass it in full:
  `CHeader('foo')` becomes `CHeader('DRIVER_FOO_H')`.
- `AddInclude` takes `system=False` for local `#include "..."` includes.
- `CEnum` now generates `enum` instead of the C++-only `enum class`.
- `CText('')` no longer crashes, and lines that start with `[` are indented.
- Class members and namespace items are indented correctly no matter what
  order they were added in.
- Generated files have a consistent blank line between sections, no stray blank
  lines and no trailing whitespace.
- Fixed swapped `argc`/`argv` in the examples.
- Added unit tests with 100% branch coverage, and a Docker image that compiles
  the generated code for every language.

## License

Apache License 2.0. See [LICENSE](LICENSE).
