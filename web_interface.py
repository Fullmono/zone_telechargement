#!/usr/bin/env python

import sys
import os
import subprocess
import re
import configparser
try:
        from flask import Flask, render_template, request, redirect, url_for
except ImportError:
        print("flask module not found")
        sys.exit(1)

app = Flask(__name__)

listeSeries = {}

def update_liste(config_file):
        """update dictionnary with list of shows, based on config_file"""
        shows_list = {}
        for series in config_file.sections():
                shows_list[series] = {'name' : str(series),
                                      'last_link' : str(config_file[series]['last_episode']),
                                      'link' : str(config_file[series]['link'])}
        return shows_list

def check_config(configfile):
        """check if config is ok"""
        if os.path.isfile(configfile):
                config = configparser.ConfigParser()
                config.read(configfile)
                listeSeries = update_liste(config)
        else:
                print ("no config found")
                config = None
        return config

config = check_config('config.ini')

if config == None:
        print('Pas de configuration trouvée')
        sys.exit()

templateData = {}

@app.route("/", methods = ['POST', 'GET'])
def main():
        """main page display display list of items of no parameters"""
        global templateData
        global config
        config = check_config('config.ini')
        listeSeries = update_liste(config)
        templateData['series'] = listeSeries
        if request.values.get('check_now') == 'check':
                try:
                        retcode = subprocess.check_output(['python', 'zone_telechargement.py'], universal_newlines=True)
                        templateData['message'] = str(retcode).split('\n')
                except subprocess.CalledProcessError as e:
                        templateData['message'] = str('erreur d\'éxecution\n' + str(e.output)).split('\n')
        return render_template('main.html', **templateData)


@app.route("/<serie>", methods = ['POST', 'GET'])
def edit_form(serie):
        """page for editing info for a specific show"""
        global templateData
        global config
        config = check_config('config.ini')
        if serie in config.sections():
                templateData = {'name' : serie,
                                'last_episode': str(config[serie]['last_episode']),
                                'link' : str(config[serie]['link'])}
        else:
                templateData = {'message' : ['serie ' + str(serie) + ' non trouvée']}
        if request.values.get('delete') == 'Effacer':
                if config.has_section(templateData['name']):
                        print ('série : ' + templateData['name'])
                        config.remove_section(templateData['name'])
                        templateData = {'message' : ['serie ' + str(serie) + ' effacée']}
                        with open('config.ini', 'w') as fichierconfig:
                                config.write(fichierconfig)
                        return redirect(url_for('main'))
                else:
                        templateData['message'] = ['cette série n\'existe pas']
        return render_template('editserie.html', **templateData)

@app.route("/internal/new", methods = ['POST', 'GET'])
def new_entry():
        """page for adding a new show to the list"""
        global templateData
        global config
        templateData = {}
        if request.values.get('valider') == 'Valider':
                templateData = {'name' : str(request.values.get('name')).lstrip().rstrip(),
                                'last_episode' : str(request.values.get('last_episode').strip()),
                                'link' : str(request.values.get('link')).strip()}
                if templateData['name'] == '':
                        templateData['message'] = ['nom de série invalide']
                        return render_template('newserie.html', **templateData)
                if templateData['last_episode'] == '':
                        templateData['message'] = ['numéro d\'épisode invalide']
                        return render_template('newserie.html', **templateData)
                if templateData['link'] == '':
                        templateData['message'] = ['lien de la série invalide']
                        return render_template('newserie.html', **templateData)
                if config.has_section(templateData['name']):
                        templateData['message'] = ['cette série existe déjà dans la liste, changer le nom']
                        return render_template('newserie.html', **templateData)
                config.add_section(templateData['name'])
                config[templateData['name']]['link'] = templateData['link']
                config[templateData['name']]['last_episode'] = templateData['last_episode']
                with open('config.ini', 'w') as fichierconfig:
                        config.write(fichierconfig)
                templateData['message'] = ['serie ' + templateData['name'] + ' a été ajoutée']
                return redirect(url_for('main'))
        return render_template('newserie.html', **templateData)

@app.route("/internal/config", methods = ['POST', 'GET'])
def edit_config():
        global templateData
        templateData['message'] = ['pas encore implémenté']
        return redirect(url_for('main'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8090, debug=True)

