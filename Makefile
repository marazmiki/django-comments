default: dev_ext $(TARGET)

current_dir = $(shell pwd)

test:
	python setup.py test

release:
	python setup.py sdist --format=zip,bztar,gztar register upload

flake8:
	flake8 --ignore=E501 --max-complexity 12 django_comments

coverage:
	coverage run --include=django_comments/* setup.py test
	coverage html

clean:
	@echo Removing python compiling files
	@find . -name "*.pyc" -exec rm -rf {} \;
	@echo Removing package metadata
	@rm -rf *.egg-info *.egg

