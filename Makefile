.PHONY: configure make run clean

all: configure make
configure:
	pip install -r requirement.txt

make:
	@pyinstaller --onefile script.py
	@mv dist/script sway_start

run: make
	./sway_start

clean:
	@rm -rf dist build script.spec
