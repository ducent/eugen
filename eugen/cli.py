from eugen.version import __version__
from eugen.processor import Processor, DEFAULT_BUILD_DIRECTORY, DEFAULT_TEMPLATES_DIRECTORY
import click, logging

@click.command()
@click.argument('files', type=click.Path(), nargs=-1, required=True)
@click.option('-t', '--templates_directory', type=click.Path(), default=DEFAULT_TEMPLATES_DIRECTORY)
@click.option('-o', '--output_directory', type=click.Path(), default=DEFAULT_BUILD_DIRECTORY)
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.version_option(__version__)
def main(files, templates_directory, output_directory, verbose):
  """Design system documentation generator based on CSS comments.
  """

  logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)

  eugen = Processor(
    templates_directory=templates_directory, 
    build_directory=output_directory,
  )

  eugen.process(*files)
