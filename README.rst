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

  $ eugen your_css_file.css and_another.css -t templates_directory -o output_directory

Syntax
------

In order to generate the final documentation, you'll have to add some tags in your CSS comments based on what you'd expect:

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
   * `block` name, and render it in `sidebar/index.html`
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

Writing templates
-----------------

Writing templates is just as easy as the syntax itself and use `Jinja2 <http://jinja.pocoo.org/docs/2.10/templates/>`_ as its template engine. Creates a directory containing your template files (in html or `pugjs like syntax <https://github.com/ducent/spenx>`_) and eugen will use them to render your site. But how does it know which one to choose?

Here's an example. Suppose you have written something like this:

.. code-block:: css

  /**
   * @name: My topnotch design system!
   * @version: 1.0.0
   */
  :root { }

eugen will parse it and try to load the template for each tag that appears in the declaration, here **name** and **version**. So if you have defined a template called `name.html`, it will be rendered with those page data. Easy right? (by the way, the `:root` element being your index page, it will also try to call the `index.html` template file).

When generating your site, eugen will also copy the CSS files from which it has been generated to the root of the output directory. They will be made available in your templates using the `source_css` property.

Available variables
^^^^^^^^^^^^^^^^^^^

Inside a template, here is the list of available data you have access to:

- **page**: Current element being rendered (See page-data_ below)
- **site**: Generated `site object <https://github.com/ducent/eugen/blob/master/eugen/site.py>`_
- **current_url**: Current url being generated
- **source_css**: A list of string containing the final path of CSS files from which the documentation is being generated

Available Jinja filters
^^^^^^^^^^^^^^^^^^^^^^^

To make your life easier, here is the list of available Jinja fiters you can use in your template:

- **spenx(source)**: Convert a string to HTML using the spenx library
- **join(lines, separator='')**: Join an array of strings using the given separator
- **markdown(source)**: Convert a string or an array of string to HTML using the markdown library
- **url(path)**: Makes a relative url from a string, you should always use it in your templates
- **asset(path)**: Mark a path as an asset which means it will be copied to the output directory and a relative url will be used


Page data
---------

.. _page-data:

Page data are what's been parsed by eugen. Every tag is represented as a list of strings, one element corresponding to one parsed line.

.. code-block:: python

  page = {
    '_': ['Contains every comments not tied to any eugen tag', 'and may span multiple lines'],
    'url': lambda group='': 'lambda which returns the url relative to a group',
    'declarations': ['.text', 'p', '.and-every-other-declaration],
    'properties': [
      {
        '_': ['Structure is the same as for the page data', 'except the name property'],
        'name': 'name-of-the-variable',
      },
    ],
    'block': ['Contains all lines for the @block tag', 'here is another example with a @version tag'],
    'version': ['1.0.0'],
  }