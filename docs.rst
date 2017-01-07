Documentation
==============

Contributing
------------

This is github, that's what your are supposed to do here!

But where is the source code?

Usage
-----
Follow this instructions:

1. Open ``http://a-domain-name.a-tld/index/edit``
2. Use your head and ask if you don't understand what you are doing

Done, you know how to use the product. Enjoy!

What langage should I use?
---------------------------

* Before anything else, get your biggest logo, and run::

   #!/bin/bash -e

   sudo apt install imagemagick
   convert logo-big.png -geometry 30% logo.png
   convert logo.png favicon.ico

* For branding, Search Engine Optimization, accessibility: ``HTML5``
* For new features: ``Go``
* For look and feel: ``CSS``
* Letting your users know about new features: ``RSS``
* For tests: ``Python3``

* Or just do all of the above in ``javascript``!

Developer guide
---------------

* Install a good Text Editor: that's the tool you'll be using for all your refactorings

* Install the debugger, REPL and auto-completion provider

.. code-block:: console

   $ pip install ipdb
   # Or:
   $ pip install pdbpp



1. Run ``bootstrap.py``
2. Run ``dev.py``

* Press "up arrow + enter" if compilation fails
* Press "control-c" to reload
* Press "control-backspace" to edit ``dev.py``

* To debug, insert the following line:

.. code-block:: console

   import pdb; pdb.set_trace()

You are now:

* Using TDD
* Have all the IDE features you need, introspection, live-edit,
  auto-completion, ...
* You are now doing automatic QA after every change.

Congrats!

Functional tests
----------------

Install Python3.

Then:

.. code-block:console::

   pip install -r requirements.txt

.. Yeah, this one is tricky, but pipfile is coming :)

On a developer box::

  $ pytest -s -k '<user_story>'

On Jenkins::

  $ pytest --capture=yes --junit-xml=junit.xml

Deployment
----------

* Copy the binary somewhere
* Run it

Rest API
--------

You already know it

Buisness plan
-------------

Do something that does not cost much. Figure out how to earn big money after.
