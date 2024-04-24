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

    def test_extract_codeblock(self):
        file_path = get_data_path("fenced_code_block.md")
        checker = FileChecker(file_path)

        result_set = set(["https://www.markdownguide.org/extended-syntax/#fenced-code-blocks"])

        links = checker.extractHyperlinks()
        self.assertSetEqual(links, result_set)

    def test_checkMarkdown_invalid_local(self):
        checker = FileChecker.initializeByContent("[link](non_existing_file.md)")
        valid = checker.checkMarkdown()
        self.assertFalse(valid)

    def test_checkMarkdown_external_valid(self):
        # do not check if URL is reachable
        checker = FileChecker.initializeByContent("[link](http://www.non_existing_website.non_existing)")
        valid = checker.checkMarkdown()
        self.assertTrue(valid)

    def test_checkMarkdown_external_invalid(self):
        # check if URL is reachable
        checker = FileChecker.initializeByContent("[link](http://www.non_existing_website.non_existing)")
        checker.setOptions(check_url_reachable=True)
        valid = checker.checkMarkdown()
        self.assertFalse(valid)

    def test_checkMarkdown_external_with_element(self):
        # it happened that valid URL had '#' and '/' at end of the address
        checker = FileChecker.initializeByContent("[link](http://www.google.com#target-element/)")
        checker.setOptions(check_url_reachable=True)
        valid = checker.checkMarkdown()
        self.assertTrue(valid)

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
        checker.setOptions(implicit_heading_id_github=True)

        valid = checker.checkMarkdown()
        self.assertTrue(valid)

    def test_checkMarkdown_bitbucket(self):
        file_path = get_data_path("bitbucket.md")
        checker = FileChecker(file_path)
        checker.setOptions(implicit_heading_id_bitbucket=True)

        valid = checker.checkMarkdown()
        self.assertTrue(valid)

    def test_checkMarkdown_codeblock(self):
        file_path = get_data_path("fenced_code_block.md")
        checker = FileChecker(file_path)

        valid = checker.checkMarkdown()
        self.assertTrue(valid)

    # TODO: integration tests checking if real URLs are reachable
    # def test_checkURLReachable_github(self):
    #     checker = FileChecker("")
    #     checker.setOptions(check_url_reachable=True)
    #
    #     valid = checker.checkURLReachable("https://github.com/anetczuk/ros-diagram-tools")
    #     self.assertTrue(valid)
    #
    # def test_checkURLReachable_sick(self):
    #     checker = FileChecker("")
    #     checker.setOptions(check_url_reachable=True)
    #
    #     valid = checker.checkURLReachable("http://www.sick.com/")
    #     self.assertTrue(valid)
    #
    # def test_checkURLReachable_ti(self):
    #     checker = FileChecker("")
    #     checker.setOptions(check_url_reachable=True)
    #
    #     valid = checker.checkURLReachable("http://e2e.ti.com/support/arm/sitara_arm/f/791/t/277952")
    #     self.assertTrue(valid)
    #
    # def test_checkURLReachable_appveyor(self):
    #     checker = FileChecker("")
    #     checker.setOptions(check_url_reachable=True)
    #
    #     valid = checker.checkURLReachable("https://ci.appveyor.com/api/projects/status/riaj54pn4h08xy40?svg=true")
    #     self.assertTrue(valid)
    #
    # def test_checkURLReachable_epfl(self):
    #     checker = FileChecker("")
    #     checker.setOptions(check_url_reachable=True)
    #
    #     valid = checker.checkURLReachable("http://rgl.epfl.ch/people/wjakob")
    #     self.assertTrue(valid)
