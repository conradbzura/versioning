.PHONY: help tests debug-tests update-tests clean-imports

help:
# List all make targets

	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@grep -E '^[a-zA-Z_-]+:.*?$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":"}; {printf "  %-20s\n", $$1}' | sort | uniq

tests:
	pytest tests/ $(PYTEST_ARGS)

debug-tests:
	PYTEST_ARGS="--wait-for-debugger" $(MAKE) tests

update-tests:
	PYTEST_ARGS="--copy-actual-to-expected" $(MAKE) tests
