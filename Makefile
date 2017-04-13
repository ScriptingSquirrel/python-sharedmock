test_cmd = py.test
lint_cmd = prospector

install:
	$(info * Installing Python requirements...)
	pip3 install -r requirements.txt

lint:
	$(info * Running linter...)
	$(lint_cmd)

test:
	$(info * Running tests w/ coverage measurement...)
	$(test_cmd) --cov=.

testnocov:
	$(info * Running tests w/o coverage measurement...)
	$(test_cmd)

.PHONY: install lint test testnocov