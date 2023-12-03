## checkmdlinks.py --help
```
usage: checkmdlinks.py [-h] [-la] [--silence] [-d DIR] [-f N [N ...]]
                       [--excludes N [N ...]] [--implicit-heading-id-github]
                       [--implicit-heading-id-bitbucket]

check links in Markdown

optional arguments:
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
```
