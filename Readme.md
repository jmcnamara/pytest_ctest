
## Using `pytest` as a testrunner for CTEST unit test files

This is an simple tutorial on how to use the Python [`pytest`][1] testing tool as a testrunner
for [CTEST][2] unit tests.

### CTEST

CTEST is a C unit test framework. It is self contained in a single header file but also contains an integrated test runner.

It goes way beyond other macro based C unit tests frameworks while still providing a test collector and runner without external programs. It uses a large amount of C magic to do this but the end result is a lightweight yet fully functional C unit test framework.

It provides most of the functionality of [GoogleTest][9] or [Unity][10] but without the overhead of a large support framework or external scaffolding.

It also has nice clear output. Here is a example from the sample unit test in the CTEST repo:

![image][3]

### Pytest

CTEST has its own test runner and, as already stated, it is standalone and doesn't need external scaffolding apart from a simple `main()`.

Nevertheless, the example shown here used [`Pytest`][4] as a test runner for CTEST. This offers a small amount of additional functionality to CTEST and is presented mainly as a proof of concept.

`Pytest` is a really nice Python testing tool. It has great [documentation][5], clean code, lots of tests, a large but clear set of options for running tests and collecting results and best of all it is easily extensible.

Pytest supports the creation of hooks in a file called `conftest.py`. This allows you to define, in Python, code to find test files, run them, and collect the results. The nice thing about this is that you can create a hook layer between pytest and the CTEST unit tests without changing code in either one.

Here is the same, unmodified, CTEST test case run under pytest:

![image][6]

Pytest allows a large range of filter and commandline options such as the following to give a minimal test output:


![image][7]

### How it works

The pytest hooks are contained in the [`conftest.py`][11] program and are explained as a general concept in [Using pytest as a testrunner for C unit tests][8].



[1]: http://pytest.org/latest/index.html
[2]: https://github.com/bvdberg/ctest
[3]: https://raw.githubusercontent.com/jmcnamara/pytest_ctest/master/docs/images/ctest1.png
[4]: http://pytest.org/latest/index.htm
[5]: http://pytest.org/latest/contents.html#toc
[6]: https://raw.githubusercontent.com/jmcnamara/pytest_ctest/master/docs/images/pytest1.png
[7]: https://raw.githubusercontent.com/jmcnamara/pytest_ctest/master/docs/images/pytest2.png
[8]: http://pytest-c-testrunner.readthedocs.org/index.html
[9]: http://throwtheswitch.org/white-papers/unity-intro.html
[10]: https://code.google.com/p/googletest/
[11]: https://github.com/jmcnamara/pytest_ctest/blob/master/conftest.py
