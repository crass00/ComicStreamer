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

from database import Comic

class Blacklist(threading.Thread):
    def __init__(self, dm):
        super(Blacklist, self).__init__()

        self.queue = Queue.Queue(0)
        self.quit = False
        self.dm = dm
        
    def stop(self):
        self.quit = True
        self.join()

    def blacklister(self, file):
        import hashlib
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()
        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        print(hasher.hexdigest())
        return hasher.hexdigest()

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
    
            obj = session.query(Comic).filter(Comic.id == int(comic_id)).first()
            if obj is not None:
                try:
                    if pagenum.lower() == "remove":
                        obj.lastread_ts =  None
                        obj.lastread_page = None
                    elif int(pagenum) < obj.page_count:
                        obj.lastread_ts = datetime.datetime.utcnow()
                        obj.lastread_page = int(pagenum)
                        #logging.debug("blacklist: about to commit boommak ts={0}".format(obj.lastread_ts))
                except Exception:
                    logging.error("Blacklist: Problem blocking page {} on comic {}".format(pagenum, comic_id))
                else:
                    session.commit()
                    
            session.close()

#-------------------------------------------------

