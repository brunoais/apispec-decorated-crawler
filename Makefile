ifdef ComSpec
	OS="WIN"
else
	OS="UNIX"
endif

package:
	python setup.py sdist bdist_wheel

test-deploy:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy:
ifeq ($(OS), "WIN")
	set /p  ans="This is the real deploy. Are you sure? "
else
	@echo -n "This is the real deploy. Are you sure? " && read ans && [ $$ans == y ]
endif
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
