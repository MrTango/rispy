History
=======

v0.5 (2020-02-21)
-----------------

New features:

* Rename the package from `RISpy` to `rispy` (PEP8 https://www.python.org/dev/peps/pep-0008/#package-and-module-names)
* Added the ability to write RIS files (via `dump`) in addition to read (@J535D165)
* Code formatting rules via black and flake8
* Github actions - code formatting check and unit-tests

Breaking changes:

* Rename package from `RISparser` to `rispy`
* Revise API for reading RIS files to mirror python APIs (like `json`, `pickle`)
* `SE` RIS key mapped to `section` instead of `version` (per wikipedia_)
* `NV` RIS key mapped to `number_of_volumes` instead of `number_of_Volumes`
* `N2` RIS key mapped to `notes_abstract` instead of `abstract`
* Python ≥ 3.6 required

.. _wikipedia: https://en.wikipedia.org/wiki/RIS_(file_format)

v0.4.3 (2018-04-10)
-------------------
* Allow for blank lines at beginning of input file [fixes #3]


v0.4.2 (2017-05-29)
-------------------
* parser saves unknown tags into an ``unknown_tag`` key in dict
* python2/3 compatible
* Notes (N1) is now a ListType
* Documented testing with pytest
* Remove unused dependency peppercorn
