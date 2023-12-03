# Copyright (c) 2022, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import unittest
import logging

from mdlinkscheck import extract_links, extract_hyperlinks, extract_imgs
from mdlinkscheck import verify

from testmdlinkscheck.data import get_data_path


_LOGGER = logging.getLogger(__name__)


class APITest(unittest.TestCase):
    def test_extract_links(self):
        links_example_path = get_data_path("empty.md")
        links_set = extract_links(links_example_path)

        self.assertSetEqual(links_set, set())

    def test_extract_hyperlinks(self):
        links_example_path = get_data_path("links.md")
        links_set = extract_hyperlinks(links_example_path)

        result_set = set(
            [
                "http://www.google.com",
                "www.google.com",
                "other_file.md",
                "/tmp/other_file.md",
                "..",
                "images.md",
                "#",
                "#top",
                "#xxx",
                "images.md#subsection_example",
                "links.md#subsection_example",
                "#subsection_example",
                "#another_subsection",
                "mailto:xxx@yyy.zzz",
                "https://www.w3schools.com",
            ]
        )

        self.assertSetEqual(links_set, result_set)

    def test_extract_imgs(self):
        links_example_path = get_data_path("images.md")
        links_set = extract_imgs(links_example_path)

        result_set = set(
            ["http://www.example.com/image.gif", "../image.gif", "http://www.example.com/image.gif", "img_girl2.jpg"]
        )

        self.assertSetEqual(links_set, result_set)

    # ==========================================================================

    def test_verify_hyperlinks(self):
        links_example_path = get_data_path("links.md")
        invalid_links_set = verify(links_example_path)

        result_set = set(["www.google.com", "other_file.md", "/tmp/other_file.md", "#xxx"])

        self.assertSetEqual(invalid_links_set, result_set)

    def test_verify_imgs(self):
        links_example_path = get_data_path("images.md")
        invalid_links_set = verify(links_example_path)

        result_set = set(["../image.gif", "img_girl2.jpg"])

        self.assertSetEqual(invalid_links_set, result_set)

    def test_verify_github(self):
        links_example_path = get_data_path("github.md")
        invalid_links_set = verify(links_example_path, implicit_heading_github=True)

        result_set = set([])

        self.assertSetEqual(invalid_links_set, result_set)

    def test_verify_bitbucket(self):
        links_example_path = get_data_path("bitbucket.md")
        invalid_links_set = verify(links_example_path, implicit_heading_bitbucket=True)

        result_set = set([])

        self.assertSetEqual(invalid_links_set, result_set)
