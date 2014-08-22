###############################################################################
#
# Simple py.test test runner for CTest unit tests..
#
# Copyright 2014, John McNamara, jmcnamara@cpan.org
#
import subprocess
import pytest
import os


def pytest_collect_file(parent, path):
    """
    A hook into py.test to collect CTest executable files.

    """

    # Change this if required to match the test files in your build system.
    if path.basename.startswith("test") and path.ext == "":
        return CTestFile(path, parent)


class CTestFile(pytest.File):
    """
    A custom file handler class for C unit test files.

    """

    def collect(self):
        """
        Overridden collect method to collect the results from each
        C unit test executable.

        """
        # Get the CTest exe file and capture the output.
        test_exe = str(self.fspath)

        # Capture CTest output for tests without fails (no exception) and tests
        # with failures (with an exception).
        try:
            test_output = subprocess.check_output(test_exe)
        except subprocess.CalledProcessError, e:
            test_output = e.output

        # Clean up the unit test output for easier parsing.
        lines = test_output.split("\n")
        lines = [line.strip() for line in lines]

        # Extract the test metadata from the unit test output.
        test_results = []
        for line in lines:

            # Match the CTest default output.
            if line.startswith("TEST"):
                tokens = line.split()
                test_name = tokens[2]
                condition = tokens[-1]
                suite_name, test_name = test_name.split(":")

                condition = condition.strip('[]')

                if condition not in ("OK", "FAIL", "SKIPPED"):
                    condition = "FAIL"

                # Store the test result and metadata.
                test_results.append({"condition": condition,
                                     "suite_name": suite_name,
                                     "test_name": test_name,
                                     "file_name": "unknown_file",
                                     "line_number": 0,
                                     "error": '(no error data found)'})

            # Collect additional information for failed test results and add
            # it to the previous "FAIL" data dict.
            if line.startswith("ERR:"):
                _, test_name, error = line.split(" ", 2)

                if ":" in test_name:
                    file_name, line_number = test_name.split(":")
                    test_results[-1]["file_name"] = file_name
                    test_results[-1]["line_number"] = int(line_number)
                    test_results[-1]["error"] = error.lstrip()

            # The OK output may occasionally be on a separate line due to
            # newlines in the test output.
            if line.startswith("[OK]"):
                test_results[-1]["condition"] = "OK"

        # Yield a test case result to the py.test runner.
        for test_result in test_results:
            yield CTestItem(test_result["test_name"], self, test_result)


class CTestItem(pytest.Item):
    """
    Pytest.Item subclass to handle each test result item. There may be
    more than one test result from a test function.

    """

    def __init__(self, name, parent, test_result):
        """Overridden constructor to pass test results dict."""
        super(CTestItem, self).__init__(name, parent)
        self.test_result = test_result

    def runtest(self):
        """The test has already been run. We just evaluate the result."""
        if self.test_result["condition"] == "FAIL":
            raise CTestException(self, self.name)

        if self.test_result["condition"] == "SKIPPED":
            raise pytest.skip.Exception("CTEST_SKIP()")


    def repr_failure(self, exception):
        """
        Called when runtest() raises an exception. The method is used to format
        the output of the failed test result.

        """
        if isinstance(exception.value, CTestException):
            return ("Test failed : {suite_name}:{test_name} "
                    "at {file_name}:{line_number}\n"
                    "       error: {error}\n".format(**self.test_result))

    def reportinfo(self):
        """Called to display header information about the test case."""
        return self.fspath, self.test_result["line_number"] - 1, self.name


class CTestException(Exception):
    """Custom exception to distinguish C unit test failures from others."""
    pass
