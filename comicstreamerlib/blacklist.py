# coding=utf-8

"""
ComicStreamer blacklist manager thread class
"""

import threading
import select
import sys
import logging
import platform
import Queue
import datetime

import utils
import os

from folders import AppFolders
import database
from library import Library

class Blacklist(threading.Thread):
    def __init__(self, dm):
        super(Blacklist, self).__init__()
        self.queue = Queue.Queue(0)
        self.quit = False
        self.dm = dm
    
    def stop(self):
        self.quit = True
        self.join()

    def setBlacklist(self, comic_id, pagenum):
        # for now, don't defer the blacklist setting, maybe it's not needed
        self.actualSetBlacklist( comic_id, pagenum)
        #self.queue.put((comic_id, pagenum))
        
    def run(self):
        logging.debug("Blacklist: Started")
        pagenum = 0
        while True:
            try:
                (comic_id, pagenum) = self.queue.get(block=True, timeout=1)
            except:
                comic_id = None
                
            self.actualSetBlacklist(comic_id, pagenum)
                        
            if self.quit:
                break
            
        logging.debug("Blacklist: Stopped")

    def actualSetBlacklist(self, comic_id, pagenum):
        if comic_id is not None:
            session = self.dm.Session()
            library = Library(session)
            if pagenum == 'clear':
                library.comicBlacklist(comic_id)
            else:
                library.comicBlacklist(comic_id, pagenum)

