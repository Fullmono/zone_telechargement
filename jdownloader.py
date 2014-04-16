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

