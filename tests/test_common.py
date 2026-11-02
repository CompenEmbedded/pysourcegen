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

"""Tests for the shared building blocks (pysourcegen.common)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pysourcegen.common import Align, JoinSections, JoinWords  # noqa: E402


class TestCommon(unittest.TestCase):

    def test_align_like_gofmt(self):
        self.assertEqual(Align([['a', 'int'], ['long', 'string']]),
                         ['a    int', 'long string'])
        # A row with fewer cells ends the column run
        self.assertEqual(Align([['a', 'b', 'c'], ['x'], ['yy', 'z']]),
                         ['a b c', 'x', 'yy z'])
        self.assertEqual(Align([]), [])

    def test_join_words_and_sections(self):
        self.assertEqual(JoinWords('', 'public', '', 'class'), 'public class')
        self.assertEqual(JoinSections(['a', '', 'b']), 'a\n\nb\n')


if __name__ == '__main__':
    unittest.main()
