This repository holds a collections of various examples on how to build an energy system with oemof.
Examples are provided for each major oemof release specified by the directory they are in. Examples using the latest oemof release are:

* flexible_modelling - shows how to add an individual constraint to the oemof solph Model
* generic_chp - illustrates how the custom component `GenericCHP` can be used
* sector_coupling - jupyter notebook giving a simple example of how to couple the sectors power, heat and mobility
* simple_dispatch - shows how to set up a dispatch model
* storage_investment - example of storage capacity optimization
* variable_chp - presents how a variable combined heat and power plant (chp) works in contrast to a fixed chp

Note: You will be able to run all examples in each directory with the respective latest oemof version.
However, some examples may not work with an older minor release if they contain features the older release does not contain.
E.g., an example in the 'oemof_0.1' may have a feature introduced in v0.1.3. Thus it will work with oemof versions v0.1.3 and v0.1.4 but not with version v0.1.2.

Everybody is welcome to contribute by adding their own example, fix documentation, bugs and typos in existing models, etc via a `pull request <https://github.com/oemof/examples/pulls>`_ or by sending us an e-mail (see `here <https://oemof.org/contact/>`_ for contact information).

.. contents::
    :depth: 1
    :local:
    :backlinks: top

Installation
================

If you have a working Python3 environment, clone the examples repository and use pip to install all required packages. You have to specify the oemof version you want to install along with this.

.. code:: bash

  git clone https://github.com/oemof/oemof_examples.git
  pip install -e path/to/package[oemof/version]

For more details have a look at the `'Installation and setup' <http://oemof.readthedocs.io/en/latest/installation_and_setup.html>`_ section. There is also a `YouTube tutorial <https://www.youtube.com/watch?v=eFvoM36_szM>`_ on how to install oemof under Windows.


oemof Documentation
====================

The oemof documentation can be found at `readthedocs <http://oemof.readthedocs.org>`_. Use the `project site <http://readthedocs.org/projects/oemof>`_ of readthedocs to choose the version of the documentation. Go to the `download page <http://readthedocs.org/projects/oemof/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.

To get the latest news visit and follow our `website <https://www.oemof.org>`_.


Keep in touch
=============

You can become a watcher at our `github site <https://github.com/oemof/oemof>`_, but this will bring you quite a few mails and might be more interesting for developers. If you just want to get the latest news you can follow our news-blog at `oemof.org <https://oemof.org/>`_.


Citing oemof
============

We use the zenodo project to get a DOI for each version. `Search zenodo for the right citation of your oemof version <https://zenodo.org/search?page=1&size=20&q=oemof>`_.


License
=======

Copyright (C) 2017 oemof developing group

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
