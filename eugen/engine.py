from markdown import markdown
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, contextfilter
from spenx.ext.jinja import Spenx
from eugen.utils import copy
from os import path, makedirs
from shutil import rmtree
import logging

class Engine:
  """Represents the engine responsible of the final template rendering.
  """

  def __init__(self, build_directory, templates_directory):
    self._logger = logging.getLogger(self.__class__.__name__)
    self._build_directory = build_directory
    self._templates_directory = templates_directory
    self._current_url = None

    self._env = Environment(
      loader=FileSystemLoader(templates_directory),
      extensions=[Spenx],
    )

    self._env.filters['html'] = self._html
    self._env.filters['join'] = self._join
    self._env.filters['markdown'] = self._markdown
    self._env.filters['url'] = self._url
    self._env.filters['asset'] = self._asset
  
  def render(self, site):
    """Render the site data to the final output.

    Args:
      site (Site): Site data used to generate the output
    """

    rmtree(self._build_directory, ignore_errors=True)
    makedirs(self._build_directory, exist_ok=True)

    # Copy source css files to the build directory
    source_css = []

    for src_css in site.generated_from:
      css_name = path.basename(src_css)
      css_dest = path.join(self._build_directory, css_name)
      copy(src_css, css_dest)
      source_css.append(css_dest)
    
    for group, pages in site.groups.items():
      try:
        tpl = self._env.get_template('{}.pug'.format(group))

        self._logger.info('Rendering {} page(s) for group {}'.format(len(pages), group))

        for page in pages:
          page_url = page['url']
          page_dest = path.join(self._build_directory, page_url)

          self._logger.info('\tProcessing {}'.format(page_url))

          makedirs(path.dirname(page_dest), exist_ok=True)

          self._current_url = path.join(self._build_directory, page_url)

          html = tpl.render(page=page, current_url=page_url, site=site, source_css=source_css)

          with open(page_dest, 'w') as f:
            f.write(html)
      except TemplateNotFound:
        pass

  def _join(self, value, separator=''):
    if not isinstance(value, list):
      return value

    return separator.join(value)

  def _markdown(self, source):  
    return markdown(self._join(source, '\n'))
  
  @contextfilter
  def _url(self, context, value):
    if not path.isabs(value):
      value = path.join(self._build_directory, value)

    return path.relpath(value, path.dirname(self._current_url))

  def _asset(self, value):
    src = path.join(self._templates_directory, value)
    dest = path.join(self._build_directory, value)
    
    if copy(src, dest):
      self._logger.info('\tCopied asset file {} to {}'.format(src, dest))

    return self._url(None, dest)

  def _html(self, source):
    return self._env.extensions['spenx.ext.jinja.Spenx']._parser.parse(self._join(source, '\n'))