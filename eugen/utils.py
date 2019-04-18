from shutil import copy as shcopy, SameFileError
from os import makedirs, path

def copy(src, dest):
  """Copy source to destination and creates folders as needed.

  Args:
    src (str): Source path
    dest (str): Destination path

  Returns:
    bool: True if copy was a success, false otherwise
  """
  makedirs(path.dirname(dest), exist_ok=True)
  
  try:
    shcopy(src, dest)
    return True
  except SameFileError:
    return False