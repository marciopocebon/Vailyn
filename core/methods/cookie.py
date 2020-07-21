#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;    
    , ;   
     .   
           
       .    
     .;.    
     .;  
      :  
      ,   
       

┌─[pathtrav]─[~]
└──╼ VainlyStrain
"""

from core.methods.session import session
from http.cookiejar import FileCookieJar #MozillaCookieJar
import requests, sys, time
from core.colors import color
from core.variables import payloadlist, nullchars
from core.methods.filecheck import filecheck
from core.methods.loot import download


"""fetches cookies from the website for the cookie attack"""
def getCookie(url):
    s = session()
    s.get(url)
    return s.cookies

"""parses the cookie and lets the attacker choose the injedction point"""
def readCookie(url):
    cookie = getCookie(url)
    i = 0
    if len(cookie.keys()) < 1:
        sys.exit(color.R + "[-]" + color.END + " Server did not send any cookies.")
    for key in cookie.keys():
        print(str(i) + ": " + key)
        i += 1
    selected = input("\n[!] Select key for attack (int) :> ")
    selectedpart = list(cookie.keys())[int(selected)]
    return (cookie, selectedpart)

def cookieFromFile(cookiefile):
    jar = FileCookieJar('cookiefile')
    jar.load(ignore_expires=True)
    for cookie in jar:
        cookie.expires = time.time() + 14 * 24 * 3600
    assert(len(jar) > 0)
    return jar