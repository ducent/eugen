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

**Write** your CSS files, add some **comments** with a tiny specific syntax and provide some **templates** to generate the final documentation. Edit your styles and regenerate, your documentation will always be in sync with your actual code. Check the `example/` folder to get a grasp on how it works.

Installation
------------

.. code-block:: console

  $ pip install eugen

Usage
-----

.. code-block:: console

  $ eugen your_css_file.css and_another.css -t templates_directory -o output_directory -v

Syntax
------

In order to generate the documentation, you'll have to add some tags in your CSS comments based on what you'd expect:

.. code-block:: css

  /**
   * This is your root element, which will be rendered by the index template, it
   * represents your home.
   *
   * Here this is a simple comment not tied to a `tag`. Let's add some eugen specific
   * comments with the `@` prefix.
   *
   * @version: 1.0.0
   */
  :root {
    /**
     * Now the :root declaration has properties too which follow the same comment
     * syntax.
     *
     * @category: Colors
     *
    --brand-color: blue;
  }

  /**
   * @block
   * You can also omit the `:` and directly add the description, here, this declaration
   * is the sidebar block.
   *
   * During the rendering, each element will be grouped by every `tag` (the `@` prefix) keys
   * and a template matching that tag will be rendered for this element.
   *
   * For example, with this declaration, it will try to find a template matching the
   * `block` name, and render it in `block/sidebar/index.html`
   *
   * With this in mind, you can create your templates based on what you really need to output.
   */
  .sidebar {
  }

  /**
   * @theend
   * That's all you need to know! Easy right?
   * Everything else will be in your templates, check the `example` folder.
   */
  footer { }

Want more information, check `the full documentation <https://ducent.github.io/eugen/>`_!
