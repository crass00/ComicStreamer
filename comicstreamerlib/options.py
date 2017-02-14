import sys
import getopt
import platform
import os
import traceback

import csversion

try:
    import argparse
except:
    pass

class Options:
    help_text = """ 
Usage: {0} [OPTION]... [FOLDER LIST]

A digital comic media server.

The FOLDER_LIST is a list of folders that will be scanned recursively
for comics to add to the database (persisted)

  -p, --port           [PORT] The port the server should listen on. (persisted)
  -b, --bind             [IP] Bind server traffic to ip (persisted)
  -w, --webroot     [WEBROOT] Webroot for reverse proxy (persisted)
  -u, --user-dir     [FOLDER] Set path for user folder
  -r, --reset                 Purge the existing database and quit
  -d, --debug                 More verbose console output
  -q, --quiet                 No console output
      --nomonitor             Don't start the folder scanner/monitor
      --nobrowser             Don't launch a web browser
  -v, --version               Display version
  -h, --help                  Display this message


Example:
    comicstreamer -p 32502 --config-file ~/comcistreamer/comics.conf
    """
#   -c, --config-file    [FILE] Config file not implemented


    def __init__(self):
        self.port = None
        self.folder_list = None
        self.reset = False
        self.no_monitor = False
        self.debug = True
        self.quiet = False
        self.launch_client = True
        self.reset_and_run = False
        self.webroot = None
        self.user_dir = None
        self.bind = None
        self.extract_last_page = False
        
    def display_msg_and_quit( self, msg, code, show_help=False ):
        appname = os.path.basename(sys.argv[0])
        if msg is not None:
            print( msg )
        if show_help:
            print self.help_text.format(appname)
        else:
            print "For more help, run with '--help'"
        sys.exit(code)  

    def parseCmdLineArgs(self,remove=True):
        
        if platform.system() == "Darwin" and hasattr(sys, "frozen") and sys.frozen == 1:
            # remove the PSN ("process serial number") argument from OS/X
            input_args = [a for a in sys.argv[1:] if "-psn_0_" not in  a ]
        else:
            input_args = sys.argv[1:]
            
        # parse command line options
        try:  #will never know why the ":" is below... "dp:hrqwuvb"
            opts, args = getopt.getopt( input_args, 
                       "lhp:w:vrdqb:u:c:",
                       [ "help", "port=", "webroot=", "version", "reset", "debug", "quiet",
                    "nomonitor", "nobrowser", "bind=", "user-dir=","config-file=",
                    "_resetdb_and_run", #private
                    ] )

        except getopt.GetoptError as err:
            self.display_msg_and_quit( str(err), 2 )
        
        # process options
        for o, a in opts:
            if o in ("-r", "--reset"):
                self.reset = True
            if o in ("-d", "--debug"):
                self.debug = True                
            if o in ("-q", "--quiet"):
                self.quiet = True                
            if o in ("-h", "--help"):
                self.display_msg_and_quit( None, 0, show_help=True )
            if o in ("-p", "--port"):
                try:
                    self.port = int(a)
                except:
                    pass
            if o in ("-w", "--webroot"):
                self.webroot = a
            if o  == "-l":
                self.extract_last_page = True
            if o in ("-b", "--bind"):
                self.bind = a
            if o  == "--nomonitor":
                self.no_monitor = True
            if o  == "--nobrowser":
                self.launch_client = False                
            if o  in ("-v","--version"):
                print "ComicStreamer {0}: ".format(csversion.version)
                sys.exit(0)
            if o == "--_resetdb_and_run":
                self.reset_and_run = True
            if o in ("-u","--user-dir"):
                self.user_dir = a
            #if o in ("-c","--config-file"):
            #    self.config_file = a

        filename_encoding = sys.getfilesystemencoding()
        if len(args) > 0:
            #self.folder_list = [os.path.normpath(a.decode(filename_encoding)) for a in args]
            self.folder_list = [os.path.abspath(os.path.normpath(unicode(a.decode(filename_encoding)))) for a in args]
    
        # remove certain private flags from args
        if remove:
            try:
                sys.argv.remove("--_resetdb_and_run")
            except:
                pass


