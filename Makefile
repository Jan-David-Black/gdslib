install:
	bash install.sh

test:
	pytest

test-force:
	echo 'Regenerating metadata for regression test. Make sure there are not any unwanted regressions because this will overwrite them'
	pytest --force-regen

clean:
	rm **/**.log
	rm **/**.fsp
	rm **/**.lms

cov:
	pytest --cov=gdslib

mypy:
	mypy . --ignore-missing-imports

lint:
	flake8 gdslib

pylint:
	pylint gdslib

lintd2:
	flake8 --select RST

lintd:
	pydocstyle gdslib

doc8:
	doc8 docs/
