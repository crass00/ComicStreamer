#!/usr/bin/env python

import os
import sys
import time
import logging
import logging.handlers
import platform
import signal
import threading

import utils
from config import ComicStreamerConfig
from comicstreamerlib.folders import AppFolders
from options import Options
from server import APIServer
#from gui import GUIThread    

 
class Launcher():
    def signal_handler(self, signal, frame):
        print "Caught Ctrl-C.  exiting."
        if self.apiServer:
            self.apiServer.shutdown()
        sys.exit()
    

    
    def __init__(self):
        self.ui = None

    def exit(self):
        sys.exit()
    
    def run(self):
        
        try:
            self.apiServer.run()
        except Exception, e:
            logging.debug(e)
            self.apiServer.shutdown()
            if self.ui:
                self.ui.quit_application()
            print "I never ever had problems not exiting before, fucking python... why not exit?"
            self.exit()
            
        logging.info("I AM Start'd")
  

    def go(self):
        #utils.fix_output_encoding()
        self.apiServer = None

        opts = Options()
        opts.parseCmdLineArgs()
 
        #Configure logging
        # root level        
        logger = logging.getLogger()    
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        log_file = os.path.join(AppFolders.logs(), "ComicStreamer.log")
        if not os.path.exists(os.path.dirname(log_file)):
            os.makedirs(os.path.dirname(log_file))
        fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=1048576, backupCount=4, encoding="UTF8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        # By default only do info level to console
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    
        # set file logging according to config file
        #fh.setLevel(config['general']['loglevel'])
            
        # turn up the log level, if requested
        if opts.debug:
            sh.setLevel(logging.DEBUG)
        elif opts.quiet:
            sh.setLevel(logging.CRITICAL)
        config = ComicStreamerConfig()
        config.applyOptions(opts)

        self.apiServer = APIServer(config, opts)
    
        self.apiServer.logFileHandler = fh
        self.apiServer.logConsoleHandler = sh
        
        #signal.signal(signal.SIGINT, self.signal_handler)
    
        self.t = threading.Thread(target=self.run)
        self.t.start()
        
        #if getattr(sys, 'frozen', None):
        try:
            # A frozen app will run a GUI
            #self.apiServer.runInThread()
       
            logging.info("UI Started")
            if platform.system() == "Darwin":
                from gui_mac import MacGui
                self.ui = MacGui(self.apiServer)
                self.ui.run()
        
            elif platform.system() == "Windows":
                from gui_win import WinGui
                self.ui = WinGui(self.apiServer)
                self.ui.run()
            else:
                print "MacOS & Windows only"
        except Exception:
            if self.ui:
                self.ui.quit_application()
            self.apiServer.shutdown()

            
        logging.info("Sit you later!")

def main():
    Launcher().go()

