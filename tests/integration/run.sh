#!/bin/sh

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

# Run the unit tests with coverage, then generate a program in every
# supported language and compile, run and format-check it.
# Meant to run in the container from docker/Dockerfile:
#
#   docker build -t pysourcegen-test docker/
#   docker run --rm -v "$PWD:/src:ro" pysourcegen-test

set -eu

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
GEN="$ROOT/tests/integration"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
export PYTHONDONTWRITEBYTECODE=1 COVERAGE_FILE="$WORK/.coverage"

step() { printf '\n=== %s\n' "$*"; }

# expect_last_line <expected> <command...>: run and check the last output line
expect_last_line() {
    expected=$1; shift
    actual=$("$@" | tail -n 1 | tr -d '\r')
    if [ "$actual" != "$expected" ]; then
        echo "FAIL: expected '$expected', got '$actual'" >&2
        exit 1
    fi
    echo "$actual"
}

step 'Unit tests with branch coverage'
cd "$ROOT"
python3 -m coverage run --branch --source=src/pysourcegen \
    -m unittest discover -s tests
python3 -m coverage report --fail-under=100 --show-missing --skip-covered

cd "$WORK"

step 'C (gcc)'
python3 "$ROOT/src/hello_world_c_example.py" > hello.c
gcc -Wall -Werror -o chello hello.c
expect_last_line 'Hello World 999' ./chello

step 'C++ (g++)'
python3 "$ROOT/src/hello_world_cpp_example.py" > hello.cpp
g++ -Wall -Werror -o cpphello hello.cpp
expect_last_line 'Hello World 999' ./cpphello

step 'Rust (rustc, rustfmt)'
python3 "$ROOT/src/hello_world_rust_example.py" > hello.rs
python3 "$GEN/gen_rust.py" > full.rs
rustfmt --check --edition 2021 hello.rs full.rs
rustc --edition 2021 -D warnings -o rshello hello.rs
rustc --edition 2021 -D warnings -o rsfull full.rs
expect_last_line 'Hello World 999' ./rshello
expect_last_line 'other' ./rsfull

step 'Go (gofmt, go vet, go build)'
mkdir go && cd go
go mod init example > /dev/null 2>&1
python3 "$GEN/gen_go.py" > main.go
unformatted=$(gofmt -l .)
if [ -n "$unformatted" ]; then
    gofmt -d .
    exit 1
fi
go vet .
go build -o gofull .
expect_last_line 'bad 1 22 3 x 2' ./gofull
cd "$WORK"

step 'JavaScript (node)'
python3 "$GEN/gen_js.py" js > full.mjs
node --check full.mjs
expect_last_line 'true' node full.mjs

step 'TypeScript (tsc --strict)'
python3 "$GEN/gen_js.py" ts > full.mts
tsc --strict --noEmit false --target es2022 --module nodenext \
    --moduleResolution nodenext --outDir ts-out \
    --typeRoots "$(npm root -g)/@types" --types node full.mts
expect_last_line '1' node ts-out/full.mjs

step 'Java (javac)'
mkdir java
python3 "$GEN/gen_java.py" > java/Main.java
javac -Xlint:all -Werror -d java java/Main.java
expect_last_line '9.0 shape base rred g1 2 M 2 2' java -cp java Main

step 'C# (dotnet build, dotnet format)'
cp -r /opt/csapp cs
python3 "$GEN/gen_cs.py" > cs/Program.cs
dotnet format whitespace cs --verify-no-changes
dotnet build cs --no-restore -warnaserror -v quiet -nologo
expect_last_line '9 red 2' dotnet cs/bin/Debug/*/csapp.dll

step 'All checks passed'
