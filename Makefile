PREFIX ?= ~/.local/bin/
.PHONY: configure build run clean install

all: configure build install
configure:
	@python -m venv .venv
	@./.venv/bin/python -m pip install -r requirements.txt

build: configure
	@pyinstaller --onefile script.py
	@cp dist/script sway_start

install:
	@install -m 755 sway_start $(PREFIX)

run: build
	./sway_start

clean:
	@rm -rf dist build script.spec .venv
