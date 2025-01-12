.PHONY: tests

tests:
	pytest tests/ $(PYTEST_ARGS)

debug-tests:
	PYTEST_ARGS="--wait-for-debugger" $(MAKE) tests

update-tests:
	PYTEST_ARGS="--copy-actual-to-expected" $(MAKE) tests
