======================
SEAMM QuickMin Plug-in
======================

.. image:: https://img.shields.io/github/issues-pr-raw/molssi-seamm/quickmin_step
   :target: https://github.com/molssi-seamm/quickmin_step/pulls
   :alt: GitHub pull requests

.. image:: https://github.com/molssi-seamm/quickmin_step/workflows/CI/badge.svg
   :target: https://github.com/molssi-seamm/quickmin_step/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/molssi-seamm/quickmin_step/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/molssi-seamm/quickmin_step
   :alt: Code Coverage

.. image:: https://github.com/molssi-seamm/quickmin_step/workflows/CodeQL/badge.svg
   :target: https://github.com/molssi-seamm/quickmin_step/security/code-scanning
   :alt: Code Quality

.. image:: https://github.com/molssi-seamm/quickmin_step/workflows/Documentation/badge.svg
   :target: https://molssi-seamm.github.io/quickmin_step/index.html
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/quickmin_step.svg
   :target: https://pypi.python.org/pypi/quickmin_step
   :alt: PyPi VERSION

A SEAMM plug-in for simple, quick minimization

* Free software: BSD-3-Clause
* Documentation: https://molssi-seamm.github.io/quickmin_step/index.html
* Code: https://github.com/molssi-seamm/quickmin_step

Features
--------

QuickMin provides quick, simple optimization of molecular structures using one of a
number of forcefields. It is intended for small systems, with no more than about 300
atoms. Beyond that size it will be rather slow, but more importantly larger systems
typically have many local minima, often close to each other energetically, so the
concept of the minimum structure is not very useful.

QuickMin uses OpenBabel_ for the minimization. There are currently five forcefields
available:

  #. GAFF_ -- the general AMBER force field
  #. MMFF94_ -- the Merck molecular force field
  #. MMFF94s_ -- the Merck molecular force field for energy minimization
  #. Ghemical_
  #. UFF_ -- Universal force field

The first four have parameters for organic and biomolecular systems, while UFF attempts
to cover the entire periodic table with reasonable accuracy. The more specialized
forcefields tend to be more accurate, roughly in the order listed (though the two MMFF94
are essentially similar). By default QuickMin will try each of the forcefields in the
order given until it finds one that can handle the given molecule. You can specify the
forcefield to use; however, if it does not have parameters for your molecule, QuickMin
will throw an error.

.. _OpenBabel: http://openbabel.org/wiki/Main_Page
.. _GAFF: https://ambermd.org/antechamber/gaff.html
.. _MMFF94: https://onlinelibrary.wiley.com/doi/10.1002/%28SICI%291096-987X%28199604%2917%3A5/6%3C490%3A%3AAID-JCC1%3E3.0.CO%3B2-P
.. _MMFF94s: https://onlinelibrary.wiley.com/doi/abs/10.1002/%28SICI%291096-987X%28199905%2920%3A7%3C720%3A%3AAID-JCC7%3E3.0.CO%3B2-X
.. _Ghemical: http://bioinformatics.org/ghemical/ghemical/index.html
.. _UFF: https://pubs.acs.org/doi/10.1021/ja00051a040

Acknowledgements
----------------

This package was created with the `molssi-seamm/cookiecutter-seamm-plugin`_ tool, which
is based on the excellent Cookiecutter_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`molssi-seamm/cookiecutter-seamm-plugin`: https://github.com/molssi-seamm/cookiecutter-seamm-plugin

Developed by the Molecular Sciences Software Institute (MolSSI_), which receives funding
from the `National Science Foundation`_ under award CHE-2136142.

.. _MolSSI: https://molssi.org
.. _`National Science Foundation`: https://www.nsf.gov
