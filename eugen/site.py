from slugify import slugify
import logging

ROOT_DECLARATION = ':root'

class Site:
  """Represents the current collected site data ready to be rendered.
  """

  def __init__(self):
    self._logger = logging.getLogger(self.__class__.__name__)
    self.generated_from = []
    self.data = []
    self.groups = {}
    self.root = None
  
  def add_result(self, file, parsed_data):
    """Add a css file with the parsed data.

    Args:
      file (str): CSS file path from which data has been generated
      parsed_data (list): List of data extracted from the file
    """
    self.generated_from.append(file)
    self.data.extend(parsed_data)

    self._logger.info('Added {} data from file {}'.format(len(parsed_data), file))

  def declaration_startswith(self, declaration, elements):
    """Returns all elements for which one of their declarations starts with the
    given declaration.

    Args:
      declaration (str): Base declaration

    Returns:
      list: List of elements matching the given declaration
    """
    return [c for c in elements if any([d.startswith(declaration) for d in c['declarations']]) ]

  def _make_url(self, data):
    """Makes url for the given data object. For now, it only takes the first declaration
    and append /index.html to make pretty url or sort of at least.
    """
    first_declaration = data['declarations'][0]
    
    return '{}/index.html'.format(slugify(first_declaration))

  def compile(self):
    """Post process step. When all css data has been added to this site instance,
    compile it to create groups that will be processed by the engine by extracting
    all keys and regrouping elements.
    """

    keys = set()

    # Starts by making all urls and collecting distinct keys
    for d in self.data:
      d['url'] = self._make_url(d)

      keys = keys.union(d.keys())

    # Removes unneeded groups
    keys.discard('_')
    keys.discard('url')
    
    self.groups = { key: list(filter(lambda d: key in d, self.data)) for key in keys }

    # Try to find the :root declaration which will be the homepage of the generated website
    self.root = next(( d for d in self.data if ROOT_DECLARATION in d['declarations'] ), None)

    if self.root:
      self.root['url'] = 'index.html'

      self.groups['index'] = [self.root]

    self._logger.info('Compiled site data into {} group(s): {}'.format(len(self.groups), ', '.join(self.groups.keys())))