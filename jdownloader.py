# -*- coding: UTF-8 -*-

#This file is part of zone_telechargement.
#
#    zone_telechargement is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    zone_telechargement is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with zone_telechargement.  If not, see <http://www.gnu.org/licenses/>.
#

import re
import sys
import requests

JD_ADD_LINK = '/action/add/links/grabber(0)/start(0)/'
JD_START_DL = '/action/start'

def check_availibility(server):
    """check if the server is avaiable, exit program otherwise"""
    try:
        r = requests.get(server)
        if r.status_code == 200:
            print('Jdownloader connection OK')
    except requests.exceptions.RequestException:
            print ('Jdownloader cannot be contacted.')
            print ('Check if is it running.')
            print ('Check config server and port.')
            sys.exit()

def add_link(server, link):
    """add link to jdownloader"""
    try:
        r = requests.get(server + JD_ADD_LINK + link)
        if r.status_code == 200:
            print(r.text)
    except requests.exceptions.RequestException:
        print('cannot add link to JD')

def start_dl(server):
    """start downloads in JD"""
    try:
        r = requests.get(server + JD_START_DL)
        if r.status_code == 200:
            print (r.text)
    except requests.exceptions.RequestException:
        print('cannot start downloads in JD')

