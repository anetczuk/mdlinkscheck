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


def main(args=None):
    parser = argparse.ArgumentParser(description="check links in Markdown")
    parser.add_argument("-la", "--logall", action="store_true", help="Log all messages")
    parser.add_argument("--silence", action="store_true", help="Do not output log messages")
    parser.add_argument(
        "-d", "--dir", action="store", help="Path to directory to search .md files for for verification"
    )
    parser.add_argument(
        "-f", "--files", metavar="N", type=str, nargs="+", help="Space separated list of paths to files to check"
    )
    parser.add_argument(
        "--excludes",
        metavar="N",
        type=str,
        nargs="+",
        help="Space separated list of regex strings applied on found files to be excluded from processing",
    )
    parser.add_argument(
        "--implicit-heading-id-github",
        action="store_true",
        help="Allow links to sections with implicit id as in GitHub (lowercased ids with dashes)",
    )
    parser.add_argument(
        "--implicit-heading-id-bitbucket",
        action="store_true",
        help="Allow links to sections with implicit id as in BitBucket"
        " (lowercased ids with dashes and 'markdown-header-' prefix)",
    )
    parser.add_argument("--check-url-reachable", action="store_true", help="Check if external URLs are reachable")

    args = parser.parse_args(args=args)

    if args.silence is True:
        logging.getLogger().setLevel(logging.FATAL)
    elif args.logall is True:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.basicConfig(format="%(message)s")
        logging.getLogger().setLevel(logging.INFO)

    if not args.files and not args.dir:
        _LOGGER.error("argument required: --files or --dir")
        return 1

    md_files = find_md_files(args.dir)
    if args.files:
        md_files.extend(args.files)

    md_files = filter_items(md_files, args.excludes)

    _LOGGER.info("files to check:\n%s\n", "\n".join(md_files))

    invalid_count = 0
    for md_file in md_files:
        invalid_links = verify(
            md_file,
            implicit_heading_github=args.implicit_heading_id_github,
            implicit_heading_bitbucket=args.implicit_heading_id_bitbucket,
            check_url_reachable=args.check_url_reachable,
        )
        invalid_count += len(invalid_links)
    if invalid_count > 0:
        # errors found
        _LOGGER.info("found %s invalid links", invalid_count)
        return 1

    # everything fine
    _LOGGER.info("links valid")
    return 0
