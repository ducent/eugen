from arpeggio.cleanpeg import ParserPEG, visit_parse_tree
from eugen.visitor import Visitor

class Parser(ParserPEG):
  def __init__(self):
    super().__init__("""
root = (definition / emptyline / ignored_comment)+ EOF

EOL = r'\\n|\\r\\n'
indent = r'[ \t]*'
emptyline = indent EOL
ignored_comment = indent r'\/\*[\S\s]*?\*\/'
text = r'[^\\n\\r]+'

entity = "@" r'[a-z-_\d]+'
declaration = r'[^{\/\\n\\r,]+'
property_name = r'[a-z-\d]+'

comment_line = indent "* " entity? (": ")? text? EOL
empty_comment = indent "*" indent EOL

comment = indent "/**" EOL
  (comment_line / empty_comment)*
  indent "*/" EOL

property = comment?
  indent "--" property_name indent ":" indent r'[^;]+'

definition = comment?
  (indent declaration r'[, ]*' EOL?)+ "{" EOL?
    ((property / r'[^;}]+') r';?' EOL?)*
  "}"
""", 'root', skipws=False)

  def parse(self, source, file_name=None):
    """Parse the given input and returns the generated data.

    Args:
      source (str): Source to be parsed
    """
    return visit_parse_tree(super().parse(source), Visitor())