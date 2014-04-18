#!/usr/bin/env python

import os.path
import sys
import re
import configparser
try:
    import requests
except ImportError:
    print ("""Module requests not found.\
           \nPlease install with pip install requests""")
    sys.exit(1)
try:
    from bs4 import BeautifulSoup
except ImportError:
    print ("""Module beautifulsoup4 not found.\
           \nPlease install with pip install beautifulsoup4""")
    sys.exit(1)
import jdownloader

def get_site(site):
    """Return the html content of the site, if available"""
    try:
        r = requests.get(site)
        if r.status_code == 200:
            return r.text
    except requests.exceptions.RequestException:
            return False

def get_last_episode(html_content):
    """Return the highest episode number availabel (int)"""
    soup = BeautifulSoup(html_content)
    max = 0
    for link in soup.find_all('a', text=re.compile('Episode')):
        for s in link.string.split():
            if s.isdigit():
                number = int(s)
                if number > max:
                    max = number
    return max    

def get_link(html_content, episode):
    """Return the link of the requests episode (int)"""
    soup = BeautifulSoup(html_content)
    debut_lien = soup.find(text=re.compile(r'^' + hoster))
    lien = debut_lien.find_next('a', text=re.compile(str(episode) + r'$')).get('href')
    return lien

#MAIN
#check if config is given, or if it exists
if (len(sys.argv)) == 2:
    if (os.path.isfile(sys.argv[1])):
        configfile = sys.argv[1]
    else:
        print('no such file or directory')
        sys.exit(1)
else:
    if (os.path.isfile('config.ini')):
        configfile = 'config.ini'
    else:
        print ('no config file, please create config.ini')
        sys.exit(1)

config = configparser.ConfigParser()
config.read(configfile)

if len(config.sections()) == 0:
    print ('No available data to get files')
    sys.exit(1)

jd_server = r'http://' + config['DEFAULT']['jd_ip'] + r':' + config['DEFAULT']['jd_port']

jdownloader.check_availibility(jd_server)

hoster = config['DEFAULT']['host_id']

config_change = False

for series in config.sections():
    check = get_site(config[series]['link'])
    if check != False:
        last_episode = get_last_episode(check)
        if last_episode == config.getint(series,'last_episode'):
            print ('Last episode for ' + series + ' is up to date.')
        else:
            config_change = True
            print ('Episode(s) for ' + series + ' to be downloaded')
            for episode in range(config.getint(series,'last_episode')+1, last_episode+1):
                print(series + ' episode numero : ' + str(episode))
                lien = get_link(check, episode)
                if re.search('http', lien):
                    jdownloader.add_link(jd_server, lien)
                    config[series]['last_episode'] = str(episode)

if config_change == True:
    with open(configfile, 'w') as fichierconfig:
        config.write(fichierconfig)

