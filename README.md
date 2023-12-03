# mdlinkscheck

Simple things can be difficult. Links can be complicated. With this package headache no more.

Package verifies links in Markdown files.


## Features

- find Markdown files in subdirectories
- walk through linked Markdown files
- check standard links
- check linked images
- handle relative and absolute links, local and external resources
- handle links to elements
- check if extenal URLs are reachable
- ignore *Markdown* syntax in code blocks (*C++* lambdas syntax is simillar to *Markdown* links)


## Running

[There](doc/cmdargs.md) is description of command line arguments. To simple run execute:
```
checkmdlinks.py --dir <path-to-dir-with-MD-files>
```
Application then will go recursively and look for `.md` files and validate them. Other options include passing
particular files and setting compatibility mode with *GitHub* or *BitBucket* version of *Markdown*.


## How it works?

Library simply converts *Markdown* to *HTML* and then extracts links using *BeautifulSoup*. After that links are
verified - this is quite tricky, because links can be absolute, relative, can point to HTML element, can point to
local file or external resource. Moreover links can contain e-mail address (`mailto:`) or *JavaScript*. Even worse,
element links can point to implicit elements (*GitHub* does it in it's own way, *bitbucket* does it in different way).


## Similar projects

- [linkcheckmd](https://github.com/scivision/linkchecker-markdown) - does not validate links to element
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
