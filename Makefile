init:
	pip install -e .[dev]

upload:
	python setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf .eggs/
	rm -rf Flask_IPFS.egg-info/
	rm -rf __pycache__/
	rm -rf build/
	rm -rf dist/
