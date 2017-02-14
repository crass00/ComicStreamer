# This Makefile expects that certain GNU utils are available:
# rm, cp, grep, cut, cat

HOMEPATH ?= $(HOME)
STREAMER_BASE?= ..
STREAMER_SRC := $(STREAMER_BASE)\comicstreamerlib
DIST_DIR := $(STREAMER_BASE)\windows\dist
NSIS_CMD :=	"C:\Program Files\NSIS\Bin\makensis.exe"
VERSION := $(shell grep version "$(STREAMER_SRC)/csversion.py" | cut -d= -f2)

all: clean dist package

dist:
	cd "$(STREAMER_BASE)"
	pyinstaller -w --version-file version.py -i nsis\app.ico $(STREAMER_BASE)\comicstreamer
	cp "$(STREAMER_BASE)\comicapi\UnRAR2\UnRARDLL\unrar.dll" $(DIST_DIR)\comicstreamer
	cp -r "$(STREAMER_SRC)\gui" $(DIST_DIR)\comicstreamer
	cp -r "$(STREAMER_SRC)\static" $(DIST_DIR)\comicstreamer
	cp mutool.exe $(DIST_DIR)\comicstreamer
	
package:
	echo !define RELEASE_STR $(VERSION) > $(STREAMER_BASE)\windows\nsis\release.nsh
	$(NSIS_CMD) "$(STREAMER_BASE)\windows\nsis\comicstreamer.nsi"

clean:
	-rm -rf dist
	-rm comicstreamer.spec
	-rm -rf build
	-rm -rf nsis/release.nsh
