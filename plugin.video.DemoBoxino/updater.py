# -*- coding: utf-8 -*-
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import sys
import plugintools
import xbmc

REMOTE_VERSION_FILE = "http://"+plugintools.get_setting("server")+"/api/livetv/update/demo"
LOCAL_VERSION_FILE = os.path.join( plugintools.get_runtime_path() , "version.txt")

def check_for_updates():
    plugintools.log("boxino.updater checkforupdates")

    try:
        plugintools.log("boxino.updater remote_version_file="+REMOTE_VERSION_FILE)
        data = plugintools.read( REMOTE_VERSION_FILE )

        versiondescargada = data.splitlines()[0]
        urldescarga = data.splitlines()[1]
        plugintools.log("boxino.updater version descargada="+versiondescargada)
        
        # Lee el fichero con la versión instalada
        plugintools.log("boxino.updater local_version_file="+LOCAL_VERSION_FILE)
        infile = open( LOCAL_VERSION_FILE )
        data = infile.read()
        infile.close();

        versionlocal = data.splitlines()[0]
        plugintools.log("boxino.updater version local="+versionlocal)

        if int(versiondescargada)>int(versionlocal):
            plugintools.log("boxino.updater update found")
            
            yes_pressed = plugintools.message_yes_no("Boxino IPTV","An update is available!","Do you want to install it now?")

            if yes_pressed:
                try:
                    plugintools.log("boxino.updater Download file...")
                    local_file_name = os.path.join( plugintools.get_data_path() , "update.zip" )
                    urllib.urlretrieve(urldescarga, local_file_name )
            
                    # Lo descomprime
                    plugintools.log("boxino.updater Unzip file...")

                    import ziptools
                    unzipper = ziptools.ziptools()
                    destpathname = xbmc.translatePath( "special://home/addons/plugin.video.supMC")
                    plugintools.log("boxino.updater destpathname=%s" % destpathname)
                    unzipper.extract( local_file_name , destpathname )
                    
                    # Borra el zip descargado
                    plugintools.log("boxino.updater borra fichero...")
                    os.remove(local_file_name)
                    plugintools.log("boxino.updater ...fichero borrado")

                    xbmc.executebuiltin((u'XBMC.Notification("Updated", "The add-on has been updated", 2000)'))
                    xbmc.executebuiltin( "Container.Refresh" )
                except:
                    xbmc.executebuiltin((u'XBMC.Notification("Not updated", "An error causes the update to fail", 2000)'))

    except:
        import traceback
        plugintools.log(traceback.format_exc())
