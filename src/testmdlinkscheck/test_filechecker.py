# Copyright (c) 2022, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest
import logging

from mdlinkscheck.filechecker import FileChecker

from testmdlinkscheck.data import get_data_path


_LOGGER = logging.getLogger(__name__)


class FileCheckerTest(unittest.TestCase):
    def test_extract_links(self):
        checker = FileChecker.initializeByContent("""## <a name="how_to_use"></a> How to use?""")
        links = checker.extractHyperlinks()
        self.assertSetEqual(links, set())

    def test_checkMarkdown_multiple(self):
        file_path = get_data_path("empty.md")
        checker = FileChecker(file_path)

        valid = checker.checkMarkdown()
        self.assertTrue(valid)
        valid = checker.checkMarkdown()
        self.assertTrue(valid)

    def test_checkMarkdown_github(self):
        file_path = get_data_path("github.md")
        checker = FileChecker(file_path)

        valid = checker.checkMarkdown()
        self.assertTrue(valid)
