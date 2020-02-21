History
=======

v0.5 (2020-)
------------
* More consistent API for reading RIS files. `readris` is now load (see `json`, `pickle`, ...)
* Deprecates `readris`.
* Add functionality to dump (write) RIS files with the function dump
* Rename the package to fit the purpose and remove uppercase characters (PEP8 https://www.python.org/dev/peps/pep-0008/#package-and-module-names)

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
