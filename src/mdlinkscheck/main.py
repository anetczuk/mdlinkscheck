#
# Copyright (c) 2023, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

#
# Script checks for invalid links (a href) or invalid paths (img src) in Markdown files.
# Script converts md to html and then iterates through links and paths.
#

import os
import logging
import argparse
import re

from glob import glob

from mdlinkscheck import verify


_LOGGER = logging.getLogger(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================== CLI interface ==============================


def find_md_files(search_dir):
    ret_list = []
    for filename in glob(f"{search_dir}/**/*.md", recursive=True):
        ret_list.append(filename)
    return ret_list


def filter_items(items_list, regex_list):
    if not items_list:
        return items_list
    if not regex_list:
        return items_list

    ret_list = []
    pattern_list = [re.compile(item) for item in regex_list]
    for item in items_list:
        is_excluded = False
        for pattern in pattern_list:
            if pattern.match(item):
                is_excluded = True
                break
        if is_excluded is False:
            ret_list.append(item)

    return ret_list


def main():
    parser = argparse.ArgumentParser(description="dump tools")
    parser.add_argument("-la", "--logall", action="store_true", help="Log all messages")
    parser.add_argument("-d", "--dir", action="store", help="Path to directory to search .md files and check")
    parser.add_argument("-f", "--file", action="store", help="Path to file to check")
    parser.add_argument(
        "--excludes",
        metavar="N",
        type=str,
        nargs="+",
        help="space separated list of regex strings applied on found files to be excluded from processing",
    )

    args = parser.parse_args()

    if args.logall is True:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.basicConfig(format="%(message)s")
        logging.getLogger().setLevel(logging.INFO)

    if not args.file and not args.dir:
        _LOGGER.error("argument required: --file or --dir")
        return 1

    md_files = find_md_files(args.dir)
    if args.file:
        md_files.append(args.file)

    md_files = filter_items(md_files, args.excludes)

    _LOGGER.info("files to check:\n%s", "\n".join(md_files))

    valid = True
    for md_file in md_files:
        if verify(md_file):
            # found invalid links
            valid = False
    if valid is False:
        # errors found
        _LOGGER.info("found invalid links")
        return 1

    # everything fine
    _LOGGER.info("links valid")
    return 0
