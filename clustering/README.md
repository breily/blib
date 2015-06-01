
clustering
==========

* Implements clustering between data points based on several different distance metrics.
* Uses...


Example
-------

* See usage.py for some point sets.

    >>> import clustering
    >>> import usage
    >>> clustering.main(usage.points1)
    1       25      0.0013579       26
    3       10      0.0015404       27
    17      22      0.0028692       28
    5       15      0.0029181       29
    18      23      0.0038921       30
    7       16      0.0125628       31
    19      27      0.0136103       32
    13      20      0.0149145       33
    9       28      0.0157995       34
    11      30      0.0172042       35
    14      33      0.0288595       36
    21      26      0.0334882       37
    4       31      0.0342655       38
    8       32      0.0464498       39
    34      36      0.0522083       40
    35      37      0.0598653       41
    2       29      0.0745529       42
    38      40      0.0977870       43
    12      39      0.1166786       44
    24      43      0.1547825       45
    41      44      0.1577053       46
    6       45      0.2185767       47
    42      46      0.3085054       48
    47      48      0.4640672       49

* First and second columns are source clusters.  Third column is the distance between them.
  Fourth cluster is the new combined cluster ID.
