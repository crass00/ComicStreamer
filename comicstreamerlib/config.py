import os
import sys
import platform
import codecs
import uuid
import base64
import logging
import io
import utils

from configobj import ConfigObj
from validate import Validator

from options import Options
from comicapi.utils import which, addtopath
from comicstreamerlib.folders import AppFolders

class ComicStreamerConfig(ConfigObj):

    configspec = u"""
            [general]
            install_id=string(default="")
            folder_list=string_list(default=list())
            launch_client=boolean(default="True")
            first_run=boolean(default="True")
            [formats]
            epub=boolean(default="False")
            pdf=boolean(default="False")
            [convert]
            epub2pdf=string(default="/Applications/calibre.app/Contents/MacOS/ebook-convert")
            pdf2jpg=string(default="./mudraw")
            resolution=300
            [server]
            use_https=boolean(default="False")
            certificate_file=string(default="server.crt")
            key_file=string(default="server.key")
            port=integer(default=32500)
            webroot=string(default="")
            [security]
            use_authentication=boolean(default="False")
            username=string(default="")
            password_digest=string(default="1f81ba3766c2287a452d98a28a33892528383ddf3ce570c6b2911b0435e71940")
            use_api_key=boolean(default="False")
            api_key=string(default="")
            cookie_secret=string(default="")
            [mysql]
            active=boolean(default="False")
            database=string(default="comicdb")
            username=string(default="comic")
            password=string(default="")
            host=string(default="localhost")
            port=integer(default=3306)
            [cache]
            active=boolean(default="False")
            size=integer(default=0)
            free=integer(default=3000)
           """
    

    def __init__(self):
        super(ComicStreamerConfig, self).__init__()
               
        self.csfolder = AppFolders.settings()

        # make sure folder exisits
        if not os.path.exists( self.csfolder ):
            os.makedirs( self.csfolder )

        # set up initial values
        self.filename = os.path.join(self.csfolder, "settings")
        self.configspec=io.StringIO(ComicStreamerConfig.configspec)
        self.encoding="UTF8"
        
        # since some stuff in the configobj has to happen during object initialization,
        # use a temporary delegate,  and them merge it into self
        tmp = ConfigObj(self.filename, configspec=self.configspec, encoding=self.encoding)
        validator = Validator()
        tmp.validate(validator,  copy=True)
       
        # set up the install ID
        if tmp['general']['install_id'] == '':
            tmp['general']['install_id'] = uuid.uuid4().hex
            
        #set up the cookie secret
        if tmp['security']['cookie_secret'] == '':
            tmp['security']['cookie_secret'] = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

        # normalize the folder list
        tmp['general']['folder_list'] = [os.path.abspath(os.path.normpath(unicode(a))) for a in tmp['general']['folder_list']]
        tmp['mysql']['password'] = utils.encode(tmp['general']['install_id'],'comic')

        self.merge(tmp)
        if not os.path.exists( self.filename ):
            self.write()
            
        # not sure if this belongs here:
        # if mac app, and no unrar in path, add the one from the app bundle
        #if getattr(sys, 'frozen', None) and  platform.system() == "Darwin":
        #    if which("unrar") is None:
        #        addtopath(AppFolders.appBase())
        
    def applyOptions( self, opts ):

        modified = False
        
        if opts.port is not None:
            self['server']['port'] = opts.port
            modified = True

        if opts.folder_list is not None:
            self['general']['folder_list'] = [os.path.abspath(os.path.normpath(unicode(a))) for a in opts.folder_list]
            modified = True
        if opts.webroot is not None:
            self['server']['webroot'] = opts.webroot
            modified = True
            
        if modified:
            self.write()
