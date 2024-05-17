.. aikido documentation master file, created by
   sphinx-quickstart on Thu Jul  6 11:33:59 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. sphinx ru guide
   https://sphinx-ru.readthedocs.io/ru/latest/sphinx.html#index

.. sphinx-autobuild
   https://pypi.org/project/sphinx-autobuild/0.2.3/

Welcome to Aikido's documentation!
==================================
.. sidebar::
.. toctree::
   :maxdepth: 2
   :numbered:
   :hidden:

.. epigraph::
   *«I don't just do it because I can forget my code,
   I do it because I want to and I can.»*

   -- Denis Israfilov

.. sidebar::

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Utils
=====

Translate admin panel
---------------------
.. py:function:: translate_ru(eng="", ru="")

    Returns the English or Russian translation, depending on the LANGUAGE_CODE setting.

    If only one of the variables is specified, then returns it.
    If the eng and ru parameters are not specified, returns the boolean value of the settings LANGUAGE_CODE == "RU".

    :param eng: English word(s)
    :type eng: str or list or tuple
    :param ru: Russian translation
    :type ru: str or list or tuple
    :return: translation or bool LANGUAGE_CODE setting.
    :rtype: bool or str or list or tuple
    :raises ValueError: if length eng, ru does not match
    :raises TypeError: if eng, ru is not of str, list, tuple types

.. code-block:: python

   def translate_ru(eng="", ru=""):
       types = (str, list, tuple)

       if not (isinstance(eng, types) and isinstance(ru, types)):
           raise TypeError("Unsupported type!")

       if eng or ru:
           return ru if not eng or settings.LANGUAGE_CODE == "RU" and ru else eng

       else:
           return settings.LANGUAGE_CODE == "RU"


Packages and their purpose
==========================


That's end. Thank you for coming here.

.. d image:: _static/homepicture.jpg