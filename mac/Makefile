PYINSTALLER_CMD := pyinstaller
STREAMER_BASE ?= ..
STREAMER_SRC := $(STREAMER_BASE)/comicstreamerlib

APP_NAME := ComicStreamer
VERSION_STR := $(shell grep version $(STREAMER_SRC)/csversion.py| cut -d= -f2 | sed 's/\"//g')

MAC_BASE := $(STREAMER_BASE)/mac
DIST_DIR := $(MAC_BASE)/dist
STAGING := $(MAC_BASE)/$(APP_NAME)
APP_BUNDLE := $(DIST_DIR)/$(APP_NAME).app
APP_BUNDLE_GUI := $(APP_BUNDLE)/Contents/MacOS/gui/**/**/*.html
APP_BUNDLE_THEME := $(APP_BUNDLE)/Contents/MacOS/**/**/*.css
APP_BUNDLE_JS := $(APP_BUNDLE)/Contents/MacOS/**/**/*.js
VOLUME_NAME := $(APP_NAME)-$(VERSION_STR)
DMG_FILE := $(VOLUME_NAME).dmg

WEBHTML:=  $(patsubst %.html,%.html.small,$(wildcard $(APP_BUNDLE_GUI)))
WEBCSS :=  $(patsubst %.css,%.css.small,$(wildcard $(APP_BUNDLE_THEME)))
WEBJS  :=  $(patsubst %.js,%.js.small,$(wildcard $(APP_BUNDLE_JS)))

all: clean dist diskimage

small: clean dist html diskimage

some: clean dist

dist:
	$(PYINSTALLER_CMD) -w -s -n $(APP_NAME) $(STREAMER_BASE)/comicstreamer --noupx
	cp -a $(STREAMER_SRC)/gui $(APP_BUNDLE)/Contents/MacOS
	cp -a $(STREAMER_SRC)/static $(APP_BUNDLE)/Contents/MacOS
	cp $(MAC_BASE)/app.icns $(APP_BUNDLE)/Contents/Resources/icon-windowed.icns
	cp $(MAC_BASE)/libs/libunrar.so $(APP_BUNDLE)/Contents/MacOS
	cp $(MAC_BASE)/libs/mudraw $(APP_BUNDLE)/Contents/MacOS
	cp $(MAC_BASE)/libs/qpdf $(APP_BUNDLE)/Contents/MacOS
	
	# fix the version string in the Info.plist
	sed -i -e 's/0\.0\.0/$(VERSION_STR)/' $(MAC_BASE)/dist/$(APP_NAME).app/Contents/Info.plist

html:$(WEBCSS) $(WEBJS) $(WEBHTML)

%.html.small : %.html
	html-minifier --remove-tag-whitespace --remove-comments --remove-empty-attributes --collapse-whitespace --remove-attribute-quotes --collapse-inline-tag-whitespace -o $@ $<
	rm $<
	mv $@ $<

%.css.small : %.css
	html-minifier --remove-tag-whitespace --remove-comments --remove-empty-attributes --collapse-whitespace --remove-attribute-quotes --collapse-inline-tag-whitespace -o $@ $<
	rm $<
	mv $@ $<

%.js.small : %.js
	#html-minifier -o $@ $<
	#rm $<
	#mv $@ $<

clean:
	@rm -rf $(DIST_DIR) $(MAC_BASE)/build
	@rm -f $(MAC_BASE)/*.spec
	@rm -f logdict*.log
	@rm -f *~ *.pyc *.pyo
	@rm -f raw*.dmg
	@echo $(VERSION_STR)
diskimage:
	#Set up disk image staging folder
	rm -rf $(STAGING)
	mkdir $(STAGING)
	cp $(STREAMER_BASE)/release\ notes.txt $(STAGING)
	ln -s /Applications $(STAGING)/Applications
	cp -a $(APP_BUNDLE) $(STAGING)
	cp $(MAC_BASE)/volume.icns $(STAGING)/.VolumeIcon.icns
	SetFile -c icnC $(STAGING)/.VolumeIcon.icns

	##generate raw disk image
	rm -f $(DMG_FILE)
	hdiutil create -srcfolder $(STAGING) -volname $(VOLUME_NAME) -format UDRW -ov raw-$(DMG_FILE)	

	#remove working files and folders
	rm -rf $(STAGING)
	
	# we now have a raw DMG file.
	
	# remount it so we can set the volume icon properly
	mkdir -p $(STAGING)
	hdiutil attach raw-$(DMG_FILE) -mountpoint $(STAGING)
	SetFile -a C $(STAGING)
	
	hdiutil detach $(STAGING)
	rm -rf $(STAGING)
	
	# convert the raw image
	rm -f $(DMG_FILE)
	hdiutil convert raw-$(DMG_FILE) -format UDZO -o $(DMG_FILE)
	rm -f raw-$(DMG_FILE)
	
	#move finished product to release folder
	mkdir -p $(STREAMER_BASE)/release
	mv $(DMG_FILE) $(STREAMER_BASE)/release
	
