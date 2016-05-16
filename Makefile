
all:
	@echo nothing to do

cleandb:
	rm -f ~/.ComicStreamer/*.sqlite 

cleandbmac:
	rm -f ~/Library/Application\ Support/ComicStreamer/comicdb.sqlite 
       

clean:
	rm -f *.pyc comicstreamerlib/*.pyc comicapi/*.pyc

