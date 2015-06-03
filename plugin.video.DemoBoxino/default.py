# -*- coding: utf-8 -*-
#------------------------------------------------------------

import os
import sys
import urlparse
import plugintools
import re
import xbmcgui
import xbmcplugin
import api

THUMBNAIL_PATH = os.path.join( plugintools.get_runtime_path() , "resources" , "img" )
MAX_ITEMS_PER_PAGE = 20
plugintools.module_log_enabled = (plugintools.get_setting("debug")=="true")
plugintools.http_debug_log_enabled = (plugintools.get_setting("debug")=="true")


# Entry point
def run():
    plugintools.log("boxino.run *************************** Boxino IPTV just started ************************")
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"

    plugintools.close_item_list()


    # Main menu
def main_list(params):
    plugintools.log("boxino.main_list "+repr(params))

    if plugintools.get_setting("username")=="":
        settings(params)

    items = api.get_list(plugintools.get_setting("username") , plugintools.get_setting("password"))   
    import os
    for item in items:
            plugintools.add_item( action="livetv_by_genre", title=item["title"] , url=item["url"], thumbnail=api.get_base_url()+"img/package/"+item["title"]+".png", fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )

    plugintools.add_item( action="settings", title="Settings..." , thumbnail = os.path.join(THUMBNAIL_PATH,"thumb3.png"), folder=False )

    if plugintools.get_setting("force_advancedsettings")=="true":
        import xbmc,xbmcgui,os
        advancedsettings = xbmc.translatePath("special://userdata/advancedsettings.xml")

        if not os.path.exists(advancedsettings):
            fichero = open( os.path.join(plugintools.get_runtime_path(),"resources","advancedsettings.xml") )
            texto = fichero.read()
            fichero.close()
            
            fichero = open(advancedsettings,"w")
            fichero.write(texto)
            fichero.close()

            plugintools.message("plugin", "A new file userdata/advancedsettings.xml","has been created for optimal streaming")

    if plugintools.get_setting("check_for_updates")=="true":
        import updater
        updater.check_for_updates()

    plugintools.set_view( plugintools.LIST )

# Settings dialog
def settings(params):
    plugintools.log("boxino.settings "+repr(params))
    plugintools.open_settings_dialog()

def livetv_by_genre(params):
    plugintools.log("boxino.livetv_by_genre "+repr(params))

    next_page = get_next_page(params.get("page"))
    genre = params.get("url")
        
    items = api.get_livetv_channels_by_genre(genre)
    for item in items:
        plugintools.add_item( action="play_livetv", extra=item["id"] , title=item["title"] , url=item["url"] , thumbnail=item["thumbnail"], plot=item["plot"], fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , isPlayable=True, folder=False )
    if len(items)>=MAX_ITEMS_PER_PAGE:
        k = genre.rfind("/")
        genre = genre[:k] + "/%d" %(int(genre[k+1:]) + int(next_page))
        plugintools.add_item( action="livetv_by_genre", title=">> Next page" , url=genre , page=next_page, fanart=os.path.join(THUMBNAIL_PATH,"fanart2.jpg") , folder=True )
    xbmc.executebuiltin("Container.SetViewMode(51)")

def play_livetv(params):
    plugintools.log("boxino.play_livetv "+repr(params))

    plugintools.play_resolved_url( params.get("title"), params.get("url"), params.get("extra") )


def get_next_page(current_page):
    if current_page=="":
        current_page="0"

    next_page = str(int(current_page)+30)

    return next_page

########################################## Run This Plugin ###########################
run()



  

    