# Python HTML Parser

Simple Python HTML Parser written in pure Python able to target a specific tag (with an optional class) to be returned.

`TargettedParser` is the parser class itself; after creating an instance of it by specifying the target tag and, optionally, the target class of the tag you are looking for, you can use its `feed()` method to parse a string containing HTML. It will store the results in its `found_elements` instance variable.

## Examples

See the `main` function in `python_html_parser.py`.

## Motivation

I started to write this module because I wanted to keep a project I was developing with as few depdendencies as possible. Instead of relying on `BeautifulSoup`, that I often use, I wondered if I could write my own custom HTML parser, tailored to my needs, written in 100 % standard Python. The advantage I see in having this file in a project instead of `BeautifulSoup` is that everything is in one file

The `TargettedParser` class could be compared to BeautifoulSoup's `SoupStrainer`, but way less advanced. The advantage of this class is that everything fits in one file, which I personally like.  

## Possible improvements

- The class could easily be modified to add the ability to target any kind of attribute, but I honestly do not need it right now, so I may not do it.
- The comments could be translated in English, but this is such a small project that I do not think it is necessary right now. The functions and variables should also be self-explanatory enough. If they're not, feel free to open a discussion.