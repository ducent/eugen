from markdown import markdown
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, contextfilter
from spenx.ext.jinja import Spenx
from eugen.utils import copy, get_folder_mapping
from os import path, makedirs
from shutil import rmtree
from bs4 import BeautifulSoup
import logging

class Engine:
  """Represents the engine responsible of the final template rendering.
  """

  def __init__(self, build_directory, templates_directory):
    self._logger = logging.getLogger(self.__class__.__name__)
    self.build_directory = path.abspath(build_directory)
    self.templates_directory = path.abspath(templates_directory)

    # Here we map filenames without extensions to actual file.
    # It enables eugen to get templates without knowing exactly what extensions
    # are used.
    self._mapping = get_folder_mapping(self.templates_directory)
    self._current_url = None

    self._env = Environment(
      loader=FileSystemLoader(self.templates_directory),
      extensions=[Spenx],
    )

    # Register jinja filters
    self._env.filters['spenx'] = self._spenx
    self._env.filters['join'] = self._join
    self._env.filters['markdown'] = self._markdown
    self._env.filters['url'] = self._url
    self._env.filters['asset'] = self._asset
    self._env.filters['first'] = self._first
    self._env.filters['prettify'] = self._prettify
  
  def render(self, site):
    """Render the site data to the final output.

    Args:
      site (Site): Compiled site data used to generate the output
    """
    rmtree(self.build_directory, ignore_errors=True)

    # Copy source css files to the build directory
    source_css = []

    for src_css in site.generated_from:
      css_name = path.basename(src_css)
      css_dest = path.join(self.build_directory, css_name)
      if copy(src_css, css_dest):
        self._logger.info('Copied {} to {}'.format(css_name, css_dest))
      source_css.append(css_dest)
    
    # And process each groups
    for group, pages in site.groups.items():
      try:
        tpl = self._env.get_template(self._mapping[group])

        self._logger.info('Rendering {} page(s) for group {}'.format(len(pages), group))

        for page in pages:
          page_url = page['url'](group) # Make an url for the current type of page
          page_dest = path.join(self.build_directory, page_url)

          self._logger.info('\tProcessing {}'.format(page_url))

          makedirs(path.dirname(page_dest), exist_ok=True)

          self._current_url = page_dest

          html = tpl.render(page=page, current_url=page_url, site=site, from_css_path=source_css)

          with open(page_dest, 'w') as f:
            f.write(html)
      except (TemplateNotFound, KeyError):
        pass

  def _join(self, value, separator=''):
    """Join an array of strings using the given separator.

    Args:
      value (str or list of str): Values to join
      separator (str): Separator used to join

    Returns:
      str: Joined string

    Examples:
      >>> engine = Engine('_build', 'templates')
      >>> engine._join('a string')
      'a string'
      >>> engine._join(['multiple', 'strings'], ' ')
      'multiple strings'
      >>> engine._join(['multiple', 'values'], ', ')
      'multiple, values'
    """
    if not isinstance(value, list):
      return value

    return separator.join(value)

  def _prettify(self, value, formatter='html.parser'):
    """Prettify the given value.

    Args:
      value (str or list of str): Values to prettify
      formatter (str): Formatter used to prettify the output

    Returns:
      str: Prettified version of the value

    Examples:
      >>> engine = Engine('_build', 'templates')
      >>> engine._prettify('<html><head><title>eugen</title></head><body></body></html>')
      '<html>\\n <head>\\n  <title>\\n   eugen\\n  </title>\\n </head>\\n <body>\\n </body>\\n</html>'
    """
    return BeautifulSoup(self._join(value), formatter).prettify()

  def _first(self, value, default=''):
    """Returns the first element of a sequence or the default value.

    Args:
      value (list): Source sequence
      default (any): Default value if the sequence is empty

    Returns:
      any: The result

    Examples:
      >>> engine = Engine('_build', 'templates')
      >>> engine._first([], 'default value')
      'default value'
      >>> engine._first([5, 4, 3])
      5
    """
    return value[0] if value else default

  def _markdown(self, source):
    """Convert markdown to html.

    Args:
      source (str or list of str): Source to convert

    Returns:
      str: Html result

    Examples:
      >>> engine = Engine('_build', 'templates')
      >>> engine._markdown('**this one is strong**')
      '<p><strong>this one is strong</strong></p>'
      >>> engine._markdown(['One line', '', 'And another'])
      '<p>One line</p>\\n<p>And another</p>'
    """
    return markdown(self._join(source, '\n'))
  
  @contextfilter
  def _url(self, context, value):
    if not path.isabs(value):
      value = path.join(self.build_directory, value)

    return path.relpath(value, path.dirname(self._current_url))

  def _asset(self, value):
    src = path.abspath(path.join(self.templates_directory, value))
    dest = path.abspath(path.join(self.build_directory, value))
    
    if copy(src, dest):
      self._logger.info('\tCopied asset file {} to {}'.format(src, dest))

    return self._url(None, dest)

  def _spenx(self, source):
    """Convert the spenx source to html.

    Args:
      source (str or list of str): Source to convert
    
    Returns:
      str: Converted html

    Example:
      >>> engine = Engine('_build', 'templates')
      >>> engine._spenx(['p', '  strong A line'])
      '<p><strong>A line</strong></p>'
      >>> engine._spenx('p.content Some content in here')
      '<p class="content">Some content in here</p>'
    """
    return self._env.extensions['spenx.ext.jinja.Spenx']._parser.parse(self._join(source, '\n'))