init:
	pip install -e .[dev]

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf build/
	rm -rf dist/
