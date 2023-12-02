#!/usr/bin/env python3
#
# Copyright (c) 2023, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import logging
from typing import Set, Optional
import tempfile

import mistune

# import markdown2        # invalid conversion - converts content of code block
# import markdown         # invalid conversion - converts content of code block

import validators

from bs4 import BeautifulSoup


_LOGGER = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ===================================================================


class FileChecker:
    def __init__(self, md_path):
        self.md_file = md_path
        md_dir = os.path.dirname(md_path)
        self.md_dir = os.path.abspath(md_dir)
        self.soup: BeautifulSoup = None
        self.local_targets: Optional[Set[str]] = None
        self.valid_links = None
        self.invalid_links = None
        # load required data
        self._load()

    @staticmethod
    def initializeByContent(md_content):
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(md_content.encode("utf-8"))
            file.close()
            return FileChecker(file.name)

    def _load(self):
        with open(self.md_file, "r", encoding="utf-8") as file:
            md_content = file.read()

        tmp_dir = tempfile.gettempdir()
        tmp_dir = os.path.join(tmp_dir, "mdlinkscheck")
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_path = self.md_file.replace("/", "_")
        tmp_path = tmp_path.replace("\\", "_")
        tmp_path = f"{tmp_dir}/page_{tmp_path}.html"

        html_content = convert_md_to_html(md_content)
        with open(tmp_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        self.soup = BeautifulSoup(html_content, "html.parser")

    def _prepare(self):
        self.valid_links = set()
        self.invalid_links = set()
        if self.local_targets is None:
            self.local_targets = get_targets(self.soup)

    # return 'True' is everything ok, otherwise 'False'
    def checkMarkdown(self) -> bool:
        self._prepare()

        self._checkHyperlinks()
        self._checkImgs()

        return len(self.invalid_links) == 0

    def extractHyperlinks(self) -> Set[str]:
        ret_set = set()
        for link in self.soup.find_all("a"):
            link_href = link.get("href")
            if not link_href:
                continue
            if link_href.startswith("javascript"):
                # skip java script urls
                continue
            ret_set.add(link_href)
        return ret_set

    def extractImgs(self) -> Set[str]:
        ret_set = set()
        for img in self.soup.find_all("img"):
            img_src = img.get("src")
            if not img_src:
                continue
            ret_set.add(img_src)
        return ret_set

    # ============================================================================

    def _checkHyperlinks(self):
        """Check <a> tag."""
        links_list = self.extractHyperlinks()
        for link_href in links_list:
            if self._checkHref(link_href):
                # valid link
                self.valid_links.add(link_href)
            else:
                _LOGGER.warning("invalid link: %s in %s", link_href, self.md_file)
                self.invalid_links.add(link_href)

    def _checkImgs(self):
        """Check <img> tag."""
        links_list = self.extractImgs()
        for img_src in links_list:
            if self._checkURL(img_src):
                # valid link
                self.valid_links.add(img_src)
            else:
                _LOGGER.warning("invalid path: %s in %s", img_src, self.md_file)
                self.invalid_links.add(img_src)

    def _checkHref(self, link_href):
        if link_href == "#":
            # "back to top" special link
            return True
        if link_href == "#top":
            # "back to top" special link
            return True

        if link_href.startswith("mailto:"):
            # consider "mailto" always valid
            return True

        if self._checkURL(link_href):
            # valid file
            return True

        local_path = os.path.join(self.md_dir, link_href)
        if os.path.isdir(local_path):
            # valid directory
            return True

        target_data = link_href.split("#")
        if len(target_data) != 2:
            # invalid URL - there must be more than one # character
            return False

        # url with target
        target_url = target_data[0]
        target_label = target_data[1]
        target_label = target_label.lower()

        if not target_url:
            # local file
            if self._checkLocalTarget(target_label):
                # found local target
                return True

        # external file
        local_path = os.path.join(self.md_dir, target_url)
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, "README.md")
        if not os.path.isfile(local_path):
            # invalid file
            return False
        checker = FileChecker(local_path)
        checker._prepare()  # pylint: disable=protected-access
        return checker._checkLocalTarget(target_label)  # pylint: disable=protected-access

    def _checkURL(self, file_href):
        if validators.url(file_href):
            # valid link
            return True
        local_path = os.path.join(self.md_dir, file_href)
        if os.path.isfile(local_path):
            # valid file
            return True
        # invalid
        return False

    def _checkLocalTarget(self, target_label):
        if target_label in self.local_targets:
            # found local target
            return True
        # invalid target
        return False


def convert_md_to_html(md_content):
    # # 'escape=False' allows to embed direct HTML code into Markdown
    # html_content = mistune.markdown(file_content, escape=False)
    # return html_content

    renderer = mistune.HTMLRenderer(escape=False, allow_harmful_protocols=True)
    converter = mistune.Markdown(renderer)
    html_content = converter(md_content)
    return html_content


def get_targets(soup):
    # on GitHub headers are converted to targets
    header_labels = extract_header_labels(soup)

    header_labels_dashes = [convert_header_to_dashes(item) for item in header_labels]
    # header_labels_underscore = [convert_header_to_underscore(item) for item in header_labels]
    # bitbucket compatibility
    header_labels_bitbucket = [convert_header_to_bitbucket_target(item) for item in header_labels]

    anchor_targets = set()
    for link in soup.find_all("a"):
        link_id = link.get("id")
        if link_id:
            anchor_targets.add(link_id)
        link_name = link.get("name")
        if link_name:
            anchor_targets.add(link_name)

    ret_data = set()
    # ret_data.update(header_labels)
    ret_data.update(header_labels_dashes)
    # ret_data.update(header_labels_underscore)
    ret_data.update(header_labels_bitbucket)
    ret_data.update(anchor_targets)
    return ret_data


def convert_header_to_dashes(header_label):
    target = header_label.lower()
    target = target.replace(" ", "-")
    return target


# def convert_header_to_underscore(header_label):
#     target = header_label.lower()
#     target = target.replace(" ", "_")
#     return target


def convert_header_to_bitbucket_target(header_label):
    # bitbucket adds prefix to all section elements
    target = header_label.lower()
    target = target.replace(" ", "-")
    return f"markdown-header-{target}"


def extract_header_labels(soup):
    header_items = set()
    header_items.update(soup.find_all("h1"))
    header_items.update(soup.find_all("h2"))
    header_items.update(soup.find_all("h3"))
    header_items.update(soup.find_all("h4"))
    header_items.update(soup.find_all("h5"))
    header_items.update(soup.find_all("h6"))
    return {item.text for item in header_items}
