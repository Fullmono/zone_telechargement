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
            print('connection à jdownloader réussie')
    except requests.exceptions.RequestException:
            print ('connection à jdownloader impossible')
            print ('vérifier si jdownloader est lancé')
            print ('vérifier que jdownloader à le contrôle à distance actif')
            print ('vérifier la configuration port et serveur')
            sys.exit(1)

def add_link(server, link):
    """add link to jdownloader"""
    try:
        r = requests.get(server + JD_ADD_LINK + link)
        if r.status_code == 200:
            print(r.text)
    except requests.exceptions.RequestException:
        print('impossible de rejouter le lien à jdownloader')

def start_dl(server):
    """start downloads in JD"""
    try:
        r = requests.get(server + JD_START_DL)
        if r.status_code == 200:
            print (r.text)
    except requests.exceptions.RequestException:
        print('impossible de lancer les téléchargements sur jdowndloader')

