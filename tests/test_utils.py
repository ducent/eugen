from sure import expect
from unittest.mock import patch
from eugen.utils import get_folder_mapping
from os import path

class TestFolderMapping:
  
  def test_it_should_map_files_correctly(self):
    with patch('eugen.utils.glob', return_value=[
      '/a_path/index.html', 
      '/a_path/a_file.pug', 
      '/a_path/a_subfolder/index.html',
    ]):
      mapping = get_folder_mapping('/a_path')

      expect(mapping).to.be.a(dict)
      expect(mapping['index']).to.equal('index.html')
      expect(mapping['a_file']).to.equal('a_file.pug')
      expect(mapping[path.join('a_subfolder', 'index')]).to.equal(path.join('a_subfolder', 'index.html'))
