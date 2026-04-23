# mdlinkscheck

Simple things can be difficult. Links can be complicated. With this package headache no more.

Package verifies links in Markdown files. Typical use case is to verify *Markdown* files stored locally (e.g. as part of
project's documentation in repository).


## Features

- find Markdown files in subdirectories
- check standard links
- check linked images
- handle relative and absolute links, local and external resources
- handle links to elements
- check if external URLs are reachable
- ignore *Markdown* syntax in code blocks (*C++* lambdas syntax is similar to *Markdown* links)


## How it works?

Library simply converts *Markdown* to *HTML* and then extracts links using *BeautifulSoup*. After that links are
verified - this is quite tricky, because links can be absolute, relative, can point to HTML element, can point to
local file or external resource. Moreover links can contain e-mail address (`mailto:`) or *JavaScript*. Even worse,
element links can point to implicit elements (*GitHub* does it in it's own way, *bitbucket* does it in different way).


## Running

Application accepts following arguments:

<!-- insertstart include="doc/cmdargs.txt" pre="\n" -->
```
usage: checkmdlinks [-h] [-la] [--silence] [-d DIR] [-f N [N ...]]
                   [--excludes N [N ...]] [--implicit-heading-id-github]
                   [--implicit-heading-id-bitbucket] [--check-url-reachable]

check links in Markdown

options:
  -h, --help            show this help message and exit
  -la, --logall         Log all messages
  --silence             Do not output log messages
  -d DIR, --dir DIR     Path to directory to search .md files for for
                        verification
  -f N [N ...], --files N [N ...]
                        Space separated list of paths to files to check
  --excludes N [N ...]  Space separated list of regex strings applied on found
                        files to be excluded from processing
  --implicit-heading-id-github
                        Allow links to sections with implicit id as in GitHub
                        (lowercased ids with dashes)
  --implicit-heading-id-bitbucket
                        Allow links to sections with implicit id as in
                        BitBucket (lowercased ids with dashes and 'markdown-
                        header-' prefix)
  --check-url-reachable
                        Check if external URLs are reachable
```
<!-- insertend -->

To simple run execute:
```
checkmdlinks --dir <path-to-dir-with-MD-files>
```
or run as module:
```
python3 -m mdlinkscheck --dir <path-to-dir-with-MD-files>
```
Application then will go recursively and look for `.md` files and validate them. By passing `-f` with list of
files there is possibility to run the check against given files only. Other options include passing
particular files and setting compatibility mode with *GitHub* or *BitBucket* version of *Markdown* (anchors deduction).


## Installation

Installation of package can be done by:
 - to install using PyPI: `pip3 install --user mdlinkscheck`
 - to install package from *GitHub* downloaded ZIP file execute: `pip3 install --user -I file:mdlinkscheck-master.zip#subdirectory=src`
 - to install package directly from *GitHub* execute: `pip3 install --user -I git+https://github.com/anetczuk/mdlinkscheck.git#subdirectory=src`
 - installation from local repository root directory: `pip3 install --user .`

To uninstall run: `pip3 uninstall mdlinkscheck`

To install project under virtual environment use `tools/installvenv.sh`.

Development installation is covered in [Development](#development) section.


## Development

Project contains several tools and features that facilitate development and maintenance of the project.

In case of pull requests please run `process-all.sh --release` before the request to check installation, run tests and
perform source code static analysis.


### Installation

Installation for development with configuration of virtual environment:
  - `tools/installvenv.sh --dev` to install dependencies, the package in editable mode and install development tooling.

Installation for development without venv:
  - `src/install-app.sh --dev` to install dependencies, the package in editable mode and install development tooling.

Virtual environment can be also configured manually by:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install --upgrade pip`
  - `src/install-app.sh --dev` to install dependencies, the package in editable mode and install development tooling
or `python -m pip install -e '.[dev]'` to install project by hand.

There is also possibility to work on the project without installation. In this case project will run from local repository 
directory. This configuration requires installation of dependencies: `./src/install-deps.sh --dev`.


### Running tests

To run tests execute `src/testmdlinkscheck/runtests.py`. Code coverage can be achieved using `coverage.sh` and 
profiling can be calculated with script `profiler.sh`.


### Tools scripts

In *tools* directory there can be found following helper scripts:
- `codecheck.sh` -- static code check using several tools with defined set of rules
- `doccheck.sh` -- run `pydocstyle` with defined configuration
- `mdcheck.sh` -- check links in Markdown files
- `typecheck.sh` -- run `mypy` with defined configuration
- `checkall.sh` -- execute *check* scripts all at once
- `profiler.sh` -- profile Python scripts
- `coverage.sh` -- measure code coverate
- `notrailingwhitespaces.sh* -- as name states removes trailing whitespaces from _*.py*_ files
- `rmpyc.sh` -- remove all _*.pyc_ files

Those scripts can be run also from within virtual environment.


## Similar projects

- [linkcheckmd](https://github.com/scivision/linkchecker-markdown) - does not validate links to element (anchors)
- [markdown-link-checker](https://pypi.org/project/markdown-link-checker/) - false positives in case of links to element
- [md-url-checker](https://pypi.org/project/md-url-check/) - does not validate links to element
- [Check-That-Link](https://pypi.org/project/Check-That-Link/) - does not validate links to element
- [awesome-check-link](https://pypi.org/project/awesome-check-link/) - does not validate links to element


## References

- [HTML `a` href Attribute](https://www.w3schools.com/tags/att_a_href.asp)
- [HTML `img` src Attribute](https://www.w3schools.com/tags/att_img_src.asp)
- [Markdown format](https://www.markdownguide.org/basic-syntax/)
- [mistune](https://github.com/lepture/mistune) - Markdown to HTML conversion


## License

BSD 3-Clause License

Copyright (c) 2023, Arkadiusz Netczuk <dev.arnet@gmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
