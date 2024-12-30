PREFIX ?= ~/.local/bin/
.PHONY: configure make run clean install

all: configure make install
configure:
	@python -m venv .venv
	@./.venv/bin/python -m pip install -r requirement.txt

make:
	@pyinstaller --onefile script.py
	@cp dist/script sway_start

install:
	@install -m 755 sway_start $(PREFIX)

run: make
	./sway_start

clean:
	@rm -rf dist build script.spec .venv
