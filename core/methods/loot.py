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


┌─[Vailyn]─[~]
└──╼ VainlyStrain
"""

import sys
import os
import time
import requests

import core.variables as variables

from urllib.parse import unquote

from core.methods.session import session
from core.colors import color


date = ""


def setDate():
    global date
    # append date to folder to be unique
    if sys.platform.lower().startswith('win'):
        date = time.strftime("%Y-%m-%d %H-%M-%S")
    else:
        date = time.strftime("%Y-%m-%d %H:%M:%S")


def download(url, file, cookie=None, post=None):
    """
    download found files & save them in the loot folder
    @params:
        url    - URL to be downloaded from.
        file   - file name. (with path)
        cookie - cookie to be used.
        post   - should we do a POST request? (default: GET)
    """
    s = session()
    if cookie:
        s.cookies = cookie
    if sys.platform.lower().startswith('win'):
        if "\\" in file:
            path = '\\'.join(file.split('\\')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("\\")[0]
        else:
            path = '\\'.join(file.split('/')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("/")[0]

        # fixes directory issues on Windows, because it doesn't allow the character :, which is used in URIs
        if "@" in name:
            name = name.split("@")[1]
        name = name.split(":")[0]
        subdir = name + "-" + str(date) + "\\"
    else:
        if "\\" in file:
            path = '/'.join(file.split('\\')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("\\")[0]
        else:
            path = '/'.join(file.split('/')[0:-1])
            baseurl = url.split("://")[1]
            name = baseurl.split("/")[0]

        if "@" in name:
            name = name.split("@")[1]
        name = name.split(":")[0]
        subdir = name + "-" + str(date) + "/"
    if not os.path.exists(variables.lootdir + subdir + path):
        os.makedirs(variables.lootdir + subdir + path)
    with open((variables.lootdir + subdir + file), "wb") as loot:
        if not post:
            try:
                response = s.get(url, timeout=variables.timeout)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                print("Timeout reached looting " + url)
                return
        else:
            try:
                req = requests.Request(method='POST', url=url, data=post)
                prep = s.prepare_request(req)
                newBody = unquote(prep.body)
                prep.body = newBody
                prep.headers["content-length"] = len(newBody)
                response = s.send(prep, timeout=variables.timeout)
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                print("Timeout reached looting " + url)
                return
        loot.write(response.content)
    loot.close()
    print('{}[LOOT]{} {}'.format(color.RD, color.END + color.O + color.CURSIVE, file + color.END))
