eugen |travis| |cover| |pypi| |license|
=======================================

.. |travis| image:: https://travis-ci.org/ducent/eugen.svg?branch=master
    :target: https://travis-ci.org/ducent/eugen

.. |cover| image:: https://codecov.io/gh/ducent/eugen/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ducent/eugen

.. |pypi| image:: https://badge.fury.io/py/eugen.svg
    :target: https://badge.fury.io/py/eugen

.. |license| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0

I'm a big fan of living documentation and design systems. When building design systems using CSS, documentation can be a bit tedious and that's why I build this tiny project.

Write your CSS files, add some comments with a tiny specific syntax and provide some templates to generate the final documentation. Edit your styles and regenerate, your documentation will always be in sync with your actual code. Check the `example/` folder to get a grasp on how it works.

To keep things simple, I've ditched the HTML in favor of a more compact syntax `inspired by pugjs <https://github.com/ducent/spenx>`_. So you'll have to use it in your templates, but I promise it won't hurt you.

Installation
------------

.. code-block:: console

  $ pip install eugen

Usage
-----

.. code-block:: console

  $ eugen your_css_file.css and_another.css -t templates_directory -o output_directory

Syntax
------
