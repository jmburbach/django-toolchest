.PHONY: test 

test:
		django-admin.py test --settings=tests.settings tests
