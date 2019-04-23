from markdown import markdown
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, contextfilter
from spenx.ext.jinja import Spenx
from eugen.utils import copy, get_folder_mapping
from os import path, makedirs
from shutil import rmtree
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
      loader=FileSystemLoader(templates_directory),
      extensions=[Spenx],
    )

    self._env.filters['spenx'] = self._spenx
    self._env.filters['join'] = self._join
    self._env.filters['markdown'] = self._markdown
    self._env.filters['url'] = self._url
    self._env.filters['asset'] = self._asset
  
  def render(self, site):
    """Render the site data to the final output.

    Args:
      site (Site): Site data used to generate the output
    """
    rmtree(self.build_directory, ignore_errors=True)
    makedirs(self.build_directory, exist_ok=True)

    # Copy source css files to the build directory
    source_css = []

    for src_css in site.generated_from:
      css_name = path.basename(src_css)
      css_dest = path.join(self.build_directory, css_name)
      copy(src_css, css_dest)
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

          self._current_url = path.join(self.build_directory, page_url)

          html = tpl.render(page=page, current_url=page_url, site=site, source_css=source_css)

          with open(page_dest, 'w') as f:
            f.write(html)
      except (TemplateNotFound, KeyError):
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
      value = path.join(self.build_directory, value)

    return path.relpath(value, path.dirname(self._current_url))

  def _asset(self, value):
    src = path.abspath(path.join(self.templates_directory, value))
    dest = path.abspath(path.join(self.build_directory, value))
    
    if copy(src, dest):
      self._logger.info('\tCopied asset file {} to {}'.format(src, dest))

    return self._url(None, dest)

  def _spenx(self, source):
    return self._env.extensions['spenx.ext.jinja.Spenx']._parser.parse(self._join(source, '\n'))