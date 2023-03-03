## [argparse](https://docs.python.org/3/library/argparse.html#module-argparse) cheatsheet

#### [parser.add_argument()](https://docs.python.org/3/library/argparse.html#the-add-argument-method) method:

- _[action](https://docs.python.org/3/library/argparse.html#action)_

  |      _val_       |                                   _descr_                                    |
  | :--------------: | :--------------------------------------------------------------------------: |
  |    `'store'`     |                    _default_, stores the argument's value                    |
  | `'store_const'`  |          stores the value specified by the `const` keyword argument          |
  |  `'store_true'`  |              `True` if an argument is given, `False` otherwise               |
  | `'store_false'`  |              `False` if an argument is given, `True` otherwise               |
  |    `'append'`    | appends each argument value to the list initialized with `default` parameter |
  | `'append_const'` |   appends the value specified by the `const` keyword argument to the list    |
  |    `'extend'`    |                   extends each argument value to the list                    |
  |    `'count'`     |             counts the number of times a keyword argument occurs             |
  |     `'help'`     |                       displays help message and exits                        |
  |   `'version'`    |                          displays version and exits                          |

---

- _[nargs](https://docs.python.org/3/library/argparse.html#nargs)_

  | _val_ |      _descr_       |
  | :---: | :----------------: |
  | `"?"` | _0 or 1_ (default) |
  | `"*"` |        _0+_        |
  | `"+"` |        _1+_        |
  |  `N`  | _exact **Number**_ |

---
