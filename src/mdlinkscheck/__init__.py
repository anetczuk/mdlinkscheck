#
# Copyright (c) 2023, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

from mdlinkscheck.filechecker import FileChecker


# ============================== API interface ==============================


def verify(md_file, implicit_heading_github=False, implicit_heading_bitbucket=False):
    """Verify given Markdown file. Return list of invalid links (if any)."""
    checker = FileChecker(md_file)
    checker.setOptions(
        implicit_heading_id_github=implicit_heading_github, implicit_heading_id_bitbucket=implicit_heading_bitbucket
    )
    checker.checkMarkdown()
    return checker.invalid_links


def extract_links(md_file):
    """Extract all links from single file."""
    checker = FileChecker(md_file)
    ret_set = set()
    ret_set.update(checker.extractHyperlinks())
    ret_set.update(checker.extractImgs())
    return ret_set


def extract_hyperlinks(md_file):
    """Extract hyperlinks."""
    checker = FileChecker(md_file)
    return checker.extractHyperlinks()


def extract_imgs(md_file):
    """Extract image paths."""
    checker = FileChecker(md_file)
    return checker.extractImgs()
