from setuptools import setup, find_packages
import os

with open('README.rst', encoding='utf-8') as f:
  readme = f.read()

with open('eugen/version.py') as f:
  version = f.readline().strip()[15:-1]

setup(
  name='eugen',
  version=version,
  description='Design system documentation generator based on CSS comments',
  long_description=readme,
  url='https://github.com/ducent/eugen',
  author='Julien LEICHER',
  license='GPL-3.0',
  packages=find_packages(),
  include_package_data=True,
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Text Processing :: Markup',
  ],
  install_requires=[
    'click~=7.0',
    'Arpeggio~=1.9.0',
    'spenx~=1.1.0',
    'Jinja2~=2.10.1',
    'markdown~=3.0.1',
    'beautifulsoup4~=4.6.3',
    'unicode-slugify~=0.1.3',
    'Pygments~=2.3.1',
  ],
  extras_require={
    'test': [
      'nose~=1.3.7',
      'sure~=1.4.11',
      'coverage~=4.5.1',
    ],
  },
  entry_points={
    'console_scripts': [
      'eugen = eugen.cli:main',
    ]
  },
)