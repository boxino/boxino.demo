# -*- coding: utf-8 -*-
#------------------------------------------------------------

import os
import sys
import urlparse
import plugintools
import urllib
from xml.parsers import expat

def get_base_url():
    return "http://"+plugintools.get_setting("server")+"/"


# ---------------------------------------------------------------------------------------------------------
#  livetv
# ---------------------------------------------------------------------------------------------------------

def get_list(username, password):

    # Service call
    service_url = urlparse.urljoin(get_base_url(),"api/livetv/login/%s/%s/xbmc" %(username,password))
    
    plugintools.log("boxino.api.get_livetv_packages body="+repr(service_url))
    body , response_headers = plugintools.read_body_and_headers( service_url )

    # Response parsing
    
    items = parse_livetv_genres(body)
    plugintools.log("boxino.api.get_livetv_packages items="+repr(items))

    return items

def get_livetv_channels_by_genre(genre):

    # Service call
    service_url = genre
    #service_parameters = urllib.urlencode({'token':token,'genre':genre,'num_page':num_page,'per_page':per_page})
    body , response_headers = plugintools.read_body_and_headers( service_url )

    # Response parsing
    plugintools.log("boxino.api.get_livetv_channels_by_genre body="+repr(body))
    items = parse_livetv_channels(body)
    plugintools.log("boxino.api.get_livetv_channels_by_genre items="+repr(body))

    return items

# ---------------------------------------------------------------------------------------------------------
#  api methode 
# ---------------------------------------------------------------------------------------------------------


# parse category from xml
def parse_livetv_genres(body):

    patron = "<category>(.*?)</category>"
    packages = plugintools.find_multiple_matches(body,patron)

    items = []
    for package in packages:
        item = {}
        item["title"] = plugintools.find_single_match(package,"<genre>([^<]+)</genre>")
        item["url"] = plugintools.find_single_match(package,"<url>([^<]+)</url>")
        items.append(item)

    return items



def parse_livetv_channels(body):

    patron = "<channel>(.*?)</channel>"
    channels = plugintools.find_multiple_matches(body,patron)

    items = []
    for channel in channels:
            item = {}
            item["title"] = plugintools.find_single_match(channel,"<name>([^<]+)</name>")
            item["url"] = plugintools.find_single_match(channel,"<stream_url>([^<]+)</stream_url>")            
            item["thumbnail"] = plugintools.find_single_match(channel,"<piconname>([^<]+)</piconname>")
            item["plot"] = plugintools.find_single_match(channel,"<plot>([^<]+)</plot>")
            if item["title"]!="" and item["url"]!="":
                print "item="+str(item)
                items.append(item)
            else:
                print "item without title "+str(item)

    return items


    