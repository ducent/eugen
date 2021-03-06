from shutil import copy2, SameFileError
from os import makedirs, path
from glob import glob

def copy(src, dest): # pragma: nocover
  """Copy source to destination and creates folders as needed.

  If the destination file already exists, nothing will be done and False is returned.

  Args:
    src (str): Source path
    dest (str): Destination path

  Returns:
    bool: True if copy was a success, false otherwise or if the destination already exists
  """
  if path.isfile(dest):
    return False

  makedirs(path.dirname(dest), exist_ok=True)
  
  try:
    copy2(src, dest)
  except:
    return False

  return True

def get_folder_mapping(source):
  """Retrieve a folder mapping relative to the source folder as a dictionary 
  where keys are the name of files without extensions and without the source 
  directory.

  Args:
    source (str): source of the root folder
  """
  g = [path.relpath(p, source) for p in glob('{}/**/*.*'.format(source), recursive=True)]

  return { path.splitext(p)[0]: p for p in g }