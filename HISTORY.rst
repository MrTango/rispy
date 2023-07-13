History
=======

v0.8.0 (2023-07-13)
-------------------

Breaking changes:

* Update minimum python version from 3.6 to 3.8
* Improve URL parsing to be more robust and consistent with the spec; saved as a plural "urls" dictionary key instead of the singular "url" (@scott-8/shapiromatron #52)

Additional updates:

* Write RIS unknown tags (@simon-20 #50)

Tooling updates:

* Switch to flit
* Update black
* Switch from flake8 + isort to ruff
* Support and test python 3.8 through 3.11


v0.7.1 (2021-06-01)
-------------------

* README.rst formatting fixes

v0.7.0 (2021-06-01)
-------------------

New features:

* Allow for subclassing of readers and writers for custom implementations and greater flexibility; these custom classes can be used in all high-level commands (load/loads/dump/dumps)  (@scott-8 #36)
* Add encoding param to rispy.load if custom file encoding is needed (@scott-8 #36)
* Add convenience method to pretty-print reference type (@scott-8 #37)
* Updated setup.py and build tooling to use setup.cfg; use wheel for testing in github actions (@KOLANICH #34)
* Relicense to MIT (@shapiromatron #43)
* Support python versions 3.6, 3.7, 3.8, and 3.9 (@shapiromatron #44)
* Changed primary branch from `master` to `main`

v0.6.0 (2020-11-04)
-------------------

New features:

* Add new optional `strict=True` parameter to rispy.load/loads to allow parsing of RIS files with comments or additional metadata which aren't allowed/forbidden in spec (@ShreyRavi)
* Allow pathlib.Path objects in rispy.load in addition to file objects
* Enable multiple python environments in github test matrix (python 3.6, 3.7, and 3.8)

v0.5.1 (2020-09-29)
-------------------

New features:

* Strip BOM before processing records
* Accept ER tag without trailing whitespace

v0.5 (2020-02-21)
-----------------

New features:

* Rename the package from `RISpy` to `rispy` (PEP8 https://www.python.org/dev/peps/pep-0008/#package-and-module-names)
* Added the ability to write RIS files (via `dump`) in addition to read (@J535D165)
* Code formatting rules via black and flake8
* All methods by default return an evaluated list of references, not a generator (to be consistent w/ load/dump behavior)
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
