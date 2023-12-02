# file contains samples of generated elements ids in GitHub

GitHub automatically generates anchors for sections. Id is obtained by lowercasing section's title and replacing spaces 
with dashes. Moreover if there is more than one space between `#` and label then element id will contain additional
dash in front.

## Subsection

One word regular subsection.


## <a name="subsection_with_name"></a>Named subsection

Subsection with name tag. Watch for spaces! If there is more than one space between `#` and label then
element id will contain additional dash in front.


## Long named subsection

Subsection with long name.


## Links

All following element links are valid on GitHub:

- [link 1](#Subsection) - single word standard
- [link 2](#subsection) - single word lowercase
- [link 3](#subsection_with_name) - name tag
- [link 4](#named-subsection) - standard link to section with name tag 
- [link 5](#long-named-subsection) - lowercase long name with dashes
- [link 6](#Long-named-subsection) - long name with dashes
- <a href="#long-named-subsection">link 7</a> - direct HTML link to element

GitHub is not case sensitive.
