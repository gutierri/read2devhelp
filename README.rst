###################################################
read2devhelp: Converts README's into DeveHelp2 books
###################################################

.. image:: https://travis-ci.org/gutierri/read2devhelp.svg?branch=master
   :target: https://travis-ci.org/gutierri/read2devhelp

.. image:: https://img.shields.io/badge/code%20style-pep8-blue.svg
   :target: https://www.python.org/dev/peps/pep-0008/
   :alt: Code style: pep8

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
   :alt: Python Version: 3.6+

.. image:: https://img.shields.io/badge/dependencies-any-blue.svg
   :alt: Dependencies: Any

---------------

``read2devhelp`` leaves easy access to README~DOCS (e.g. `Axios
<https://github.com/axios/axios/>`_ JS lib), where in the library README contains necessary information that need or could be accessed offline in a structured way in `Gnome DevHelp
<https://wiki.gnome.org/Apps/Devhelp>`_.

Goodbye several tabs!


**********
Installing
**********

Via pip with git:

.. code-block:: shell

  pip3 install --user git+https://github.com/gutierri/read2devhelp.git

or save ``read2devhelp.py`` on $PATH:

.. code-block:: shell

   curl -o $HOME/.local/bin/read2devhelp https://raw.githubusercontent.com/gutierri/read2devhelp/master/read2devhelp.py

.. code-block:: shell

   chmod +x $HOME/.local/bin/read2devhelp

*****
Usage
*****

.. code-block:: shell

  read2devhelp https://github.com/axios/axios

Now just open DevHelp and the book will be there!

****
TODO
****

- Improve tag "code/pre" format code
- Support others services (e.g. gitlab, gogs, gitea, bitbucket)
- Cache images on disk
- Improve information about the book, language, author... (via command line options?)
