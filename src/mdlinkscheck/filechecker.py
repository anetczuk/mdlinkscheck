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
import hashlib

import requests
import validators

import mistune

# import markdown2        # invalid conversion - converts content of code block
# import markdown         # invalid conversion - converts content of code block

from bs4 import BeautifulSoup


_LOGGER = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ===================================================================


class FileChecker:
    def __init__(self, md_path):
        self.implicit_heading_id_github: bool = False
        self.implicit_heading_id_bitbucket: bool = False
        self.check_url_reachable: bool = False

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

    def setOptions(
        self,
        implicit_heading_id_github: bool = None,
        implicit_heading_id_bitbucket: bool = None,
        check_url_reachable: bool = None,
    ):
        if implicit_heading_id_github is not None:
            self.implicit_heading_id_github = implicit_heading_id_github
        if implicit_heading_id_bitbucket is not None:
            self.implicit_heading_id_bitbucket = implicit_heading_id_bitbucket
        if check_url_reachable is not None:
            self.check_url_reachable = check_url_reachable

    def _load(self):
        try:
            with open(self.md_file, "r", encoding="utf-8") as file:
                md_content = file.read()
        except FileNotFoundError as exc:
            _LOGGER.warning("could not open md file: %s", exc)
            return

        tmp_dir = tempfile.gettempdir()
        tmp_dir = os.path.join(tmp_dir, "mdlinkscheck")
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_path = self.md_file.replace("/", "_")
        tmp_path = tmp_path.replace("\\", "_")

        encoded_path = tmp_path.encode("utf-8")
        hash_value = hashlib.md5(encoded_path).hexdigest()  # nosec
        hash_path = f"{tmp_dir}/page_{hash_value}.html"

        html_content = convert_md_to_html(md_content)
        with open(hash_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        self.soup = BeautifulSoup(html_content, "html.parser")

    def _prepare(self):
        self.valid_links = set()
        self.invalid_links = set()
        if self.local_targets is None:
            self.local_targets = self._getElementsIds()

    # return 'True' is everything ok, otherwise 'False'
    def checkMarkdown(self) -> bool:
        self._prepare()

        self._checkHyperlinks()
        self._checkImgs()

        return len(self.invalid_links) == 0

    def checkURLReachable(self, url):
        return self._checkReachableURL(url)

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
                continue
            # invalid
            self.invalid_links.add(link_href)

    def _checkImgs(self):
        """Check <img> tag."""
        # check is 'src' points to local file or to external valid URL
        links_list = self.extractImgs()
        for img_src in links_list:
            if self._checkLocalFile(img_src):
                # valid regular file or directory
                self.valid_links.add(img_src)
                continue
            if self._checkValidURL(img_src):
                if self._checkReachableURL(img_src):
                    # valid url
                    self.valid_links.add(img_src)
                    continue

            # invalid
            _LOGGER.warning("invalid link: %s in %s", img_src, self.md_file)
            self.invalid_links.add(img_src)

    def _checkHref(self, link_href):
        if link_href.startswith("mailto:"):
            # consider "mailto" always valid
            return True

        if self._checkLocalFile(link_href):
            # valid local file
            return True
        local_dir = self._checkLocalDir(link_href)
        if local_dir:
            if not self._checkLocalREADME(local_dir):
                _LOGGER.warning("invalid path (missing README.md): %s in %s", link_href, self.md_file)
                return False
            # valid local dir
            return True

        if self._checkValidURL(link_href):
            if not self._checkReachableURL(link_href):
                _LOGGER.warning("invalid link (unreachable): %s in %s", link_href, self.md_file)
                return False
            # valid url
            return True

        target_data = link_href.split("#")
        if len(target_data) != 2:
            # invalid URL - there must be more than one # character
            _LOGGER.warning("invalid link: %s in %s", link_href, self.md_file)
            return False

        # url with target
        target_url = target_data[0]
        target_id = target_data[1]
        target_id = target_id.lower()

        if not target_url:
            # current file
            if target_id == "":
                # "back to top" special link
                return True
            if target_id == "top":
                # "back to top" special link
                return True

            if self._checkLocalTarget(target_id):
                # found local target
                return True
            _LOGGER.warning("invalid link: %s in %s", link_href, self.md_file)
            return False

        if self._checkValidURL(target_url):
            if not self._checkReachableURL(target_url):
                _LOGGER.warning("invalid link (unreachable): %s in %s", link_href, self.md_file)
                return False
            # valid url
            return True

        # other file
        local_dir = self._checkLocalDir(target_url)
        if local_dir:
            # links to directory - check if README.md exists
            local_file = self._checkLocalREADME(local_dir)
            if not local_file:
                # invalid file - missing README.md
                _LOGGER.warning("invalid path (missing README.md): %s in %s", link_href, self.md_file)
                return False
        else:
            local_file = self._checkLocalFile(target_url)
            if not local_file:
                # invalid file - missing README.md
                _LOGGER.warning("invalid path: %s in %s", link_href, self.md_file)
                return False

        # here 'local_file' points to valid file

        if target_id == "":
            # "back to top" special link
            return True
        if target_id == "top":
            # "back to top" special link
            return True

        checker = FileChecker(local_file)
        checker.setOptions(
            implicit_heading_id_github=self.implicit_heading_id_github,
            implicit_heading_id_bitbucket=self.implicit_heading_id_bitbucket,
            check_url_reachable=self.check_url_reachable,
        )
        checker._prepare()  # pylint: disable=protected-access
        if not checker._checkLocalTarget(target_id):  # pylint: disable=protected-access
            _LOGGER.warning("invalid link: %s in %s", link_href, self.md_file)
            return False
        return True

    def _checkLocalFile(self, path):
        if os.path.isfile(path):
            # valid file
            return path

        if os.path.isabs(path):
            # in Markdown there can be absolute path to file
            # the path then will be relative to repositoy's root directory
            # workaround: iterate all path parents and try if file exists
            relative_path = "." + path
            curr_path = self.md_dir
            while True:
                rel_path = os.path.join(curr_path, relative_path)
                if os.path.isfile(rel_path):
                    # valid file
                    return rel_path

                next_path = os.path.join(curr_path, os.pardir)
                next_path = os.path.normpath(next_path)
                if curr_path == next_path:
                    # end of iterations root dir reached
                    break
                curr_path = next_path

        rel_path = os.path.join(self.md_dir, path)
        if os.path.isfile(rel_path):
            # valid file
            return rel_path
        return None

    def _checkLocalREADME(self, dir_path):
        # links to directory - check if README.md exists
        local_file = os.path.join(dir_path, "README.md")
        local_file = self._checkLocalFile(local_file)
        if not local_file:
            # invalid file - missing README.md
            return None
        return local_file

    def _checkLocalDir(self, path):
        if os.path.isdir(path):
            # valid directory
            return path
        rel_path = os.path.join(self.md_dir, path)
        if os.path.isdir(rel_path):
            # valid directory
            return path
        return None

    def _checkValidURL(self, file_href):
        if not validators.url(file_href):
            # invalid
            return False
        # valid link
        return True

    def _checkReachableURL(self, url):
        if not self.check_url_reachable:
            # do not check
            return True

        try:
            headers = {"User-Agent": "My User Agent 1.0"}
            response = requests.head(url, timeout=15, headers=headers, allow_redirects=True)
            # _LOGGER.info("link %s response code: %s", url, response.status_code)
            return response.status_code == 200
        except requests.exceptions.ConnectionError:
            return False

    def _checkLocalTarget(self, target_label):
        if target_label in self.local_targets:
            # found local target
            return True
        # invalid target
        return False

    def _getElementsIds(self):
        # on GitHub headers are converted to targets
        header_labels = extract_header_labels(self.soup)

        # header_labels_underscore = [convert_header_to_underscore(item) for item in header_labels]

        anchor_targets = set()
        for link in self.soup.find_all("a"):
            link_id = link.get("id")
            if link_id:
                anchor_targets.add(link_id)
            link_name = link.get("name")
            if link_name:
                anchor_targets.add(link_name)

        ret_data = set()
        ret_data.update(anchor_targets)
        # ret_data.update(header_labels)
        # ret_data.update(header_labels_underscore)

        if self.implicit_heading_id_github:
            # github compatibility
            header_labels_github = [convert_header_to_github_target(item) for item in header_labels]
            ret_data.update(header_labels_github)

        if self.implicit_heading_id_bitbucket:
            # bitbucket compatibility
            header_labels_bitbucket = [convert_header_to_bitbucket_target(item) for item in header_labels]
            ret_data.update(header_labels_bitbucket)

        return ret_data


# =======================================================


def convert_md_to_html(md_content):
    # # 'escape=False' allows to embed direct HTML code into Markdown
    # html_content = mistune.markdown(file_content, escape=False)
    # return html_content

    renderer = mistune.HTMLRenderer(escape=False, allow_harmful_protocols=True)
    converter = mistune.Markdown(renderer)
    html_content = converter(md_content)
    return html_content


def convert_header_to_github_target(header_label):
    target = header_label.lower()
    target = target.replace(" ", "-")
    target = target.replace(",", "")
    target = target.replace(".", "")
    target = target.replace("(", "")
    target = target.replace(")", "")
    return target


# def convert_header_to_underscore(header_label):
#     target = header_label.lower()
#     target = target.replace(" ", "_")
#     return target


def convert_header_to_bitbucket_target(header_label):
    # bitbucket adds prefix to all section elements
    target = header_label.lower()
    target = target.replace(" ", "-")
    target = target.replace(",", "")
    target = target.replace(".", "")
    target = target.replace("(", "")
    target = target.replace(")", "")

    # reduce dashes
    while True:
        new_target = target.replace("--", "-")
        if new_target == target:
            # no progress - break
            break
        target = new_target

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
