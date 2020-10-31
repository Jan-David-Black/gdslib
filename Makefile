install:
	bash install.sh

lint:
	flake8 gdslib

test:
	pytest

test-force:
	echo 'Regenerating metadata for regression test. Make sure there are not any unwanted regressions because this will overwrite them'
	pytest --force-regen

clean:
	rm **/**.log
	rm **/**.fsp
	rm **/**.lms
