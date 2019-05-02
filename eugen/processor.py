from eugen.parser import Parser
from eugen.utils import copy
from eugen.site import Site
from eugen.version import __version__
from eugen.engine import Engine
from timeit import default_timer as timer
import logging

DEFAULT_TEMPLATES_DIRECTORY = 'templates'
DEFAULT_BUILD_DIRECTORY = '_build'

class Processor:
  """Main class which will orchestrate the site generation process
  """

  def __init__(self, templates_directory=DEFAULT_TEMPLATES_DIRECTORY, build_directory=DEFAULT_BUILD_DIRECTORY):
    self._logger = logging.getLogger(self.__class__.__name__)
    self._parser = Parser()
    self._engine = Engine(build_directory, templates_directory)

  def process(self, *css_files):
    start = timer()
    self._logger.info("""
-------------------------------
  Eugen version: {version}

  Processing files: {files}
  Using templates from: {templates}
  And build directory: {build}
-------------------------------""".format(
                                  version=__version__,
                                  files=', '.join(css_files), 
                                  templates=self._engine.templates_directory, 
                                  build=self._engine.build_directory))
    
    site = Site()

    for css_file in css_files:
      site.add_result(css_file, self._parser.parse_file(css_file))

    site.compile()

    self._engine.render(site)

    end = timer()

    self._logger.info('Built site in {} seconds'.format(end - start));
