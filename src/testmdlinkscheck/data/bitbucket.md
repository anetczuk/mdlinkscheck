# file contains samples of generated elements ids in BitBucket

BitBucket generates section ID by lowercasing section's title and replacing spaces with dashes then
it adds following prefix: `markdown-header-`.

See [Markdown demo](https://bitbucket.org/tutorials/markdowndemo/src/master/README.md).


## Subsection

One word regular subsection.


## <a name="subsection_with_name"></a>Named subsection

Subsection with name tag. It does not work on BitBucket, because all HTML elements are escaped.


## Long named subsection

Subsection with long name.


## Section with comma, other comma, and . here and ( and ) too

Subsection with commas, dots and other special characters.


## Links

All following element links are valid on BitBucket:

- [link 1](#markdown-header-Subsection) - single word standard
- [link 2](#markdown-header-subsection) - single word lowercase
- [link 3](#subsection_with_name) - name tag
- [link 4](#markdown-header-named-subsection) - standard link to section with name tag 
- [link 5](#markdown-header-long-named-subsection) - lowercase long name with dashes
- [link 6](#markdown-header-Long-named-subsection) - long name with dashes
- [link 7](#markdown-header-section-with-comma-other-comma-and-here-and-and-too) - section with commas and dots

BitBucket is not case sensitive.
