###############################################################################
#
# Makefile for pytest ctest testrunner.
#
# Copyright 2014, John McNamara, jmcnamara@cpan.org
#

# Keep the output quiet by default.
Q=@
ifdef V
Q=
endif

.PHONY: docs

# Build the test executables.
all :
	$(Q)CTEST_COLOR_OK=1 make -C ctest

# Clean the test executables.
clean :
	$(Q)make clean -C ctest

# Run the ctest unit tests.
test : all
	$(Q)ctest/test

pytest : all
	$(Q)py.test -v
