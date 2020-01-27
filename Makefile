init:
	pip install -e .[dev]

upload:
	python setup.py sdist bdist_wheel
	twine upload build/*

clean:
	rm -rf build/
