# Copyright (c) 2022, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest
import logging

from mdlinkscheck.main import main

from testmdlinkscheck.data import get_data_path


_LOGGER = logging.getLogger(__name__)


class MainTest(unittest.TestCase):
    def test_main_valid(self):
        md_path = get_data_path("empty.md")
        error_code = main(["--silence", "--file", md_path])

        self.assertEqual(error_code, 0)

    def test_main_invalid(self):
        md_path = get_data_path("invalid.md")
        error_code = main(["--silence", "--file", md_path])

        self.assertEqual(error_code, 1)
