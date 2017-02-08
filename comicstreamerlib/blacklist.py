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
        self.library = Library(self.dm.Session)
        
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
            if pagenum == 'clear':
                session.delete(Blacklist).filter(database.Blacklist.comic_id == int(comic_id),database.Blacklist.page == int(pagenum))
            else:
                obj = session.query(database.Blacklist).filter(database.Blacklist.comic_id == int(comic_id),database.Blacklist.page == int(pagenum)).first()
                if obj is None:
                    try:
                        blacklist = database.Blacklist()
                        image_data = self.library.getComicPage(comic_id, pagenum, False)
                        blacklist.hash = utils.hash(image_data)
                        file = open(os.path.join(AppFolders.appBlacklistPages(),str(blacklist.hash)), "w")
                        file.write(image_data)
                        file.close()
                        blacklist.comic_id = int(comic_id)
                        blacklist.page = int(pagenum)
                        blacklist.ts = datetime.datetime.utcnow()
                        session.add(blacklist)
                    except Exception, e:
                        print str(e)
                        logging.error("Blacklist: Problem blocking page {} on comic {}".format(pagenum, comic_id))

            session.commit()
            session.close()

#-------------------------------------------------

