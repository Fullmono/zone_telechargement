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

templateData = {}

@app.route("/", methods = ['POST', 'GET'])
def main():
        """main page display display list of items of no parameters"""
        global templateData
        global config
        config = check_config('config.ini')
        if config == None:
                templateData['message'] = ['pas de configuration trouvée']
                return redirect(url_for('edit_config'))
        listeSeries = update_liste(config)
        templateData['series'] = listeSeries
        if request.values.get('check_now') == 'vérifier':
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
        if config == None:
                templateData['message'] = ['pas de configuration trouvée']
                return redirect(url_for('edit_config'))
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
        if request.values.get('valider') == 'Valider':
                name = str(request.values.get('name')).strip()
                last_episode = str(request.values.get('last_episode')).strip()
                link = str(request.values.get('link')).strip()
                if name == '' or link == '':
                        templateData['message'] = ['nom ou lien invalide']
                        render_template('editserie.html', **templateData)
                if name == serie:
                        templateData['message'] = ['serie ' + serie + ' mise à jour']
                        config[serie]['link'] = link
                        if last_episode == '':
                                config[serie]['last_episode'] = config['DEFAULT']['last_episode']
                        else:
                                config[serie]['last_episode'] = last_episode
                        with open('config.ini', 'w') as fichierconfig:
                                config.write(fichierconfig)
                        return redirect(url_for('main'))
                else:
                        if config.has_section(serie):
                                config.remove_section(serie)
                        config.add_section(name)
                        config[name]['link'] = link
                        if last_episode == '':
                                config[name]['last_episode'] = config['DEFAULT']['last_episode']
                        else:
                                config[name]['last_episode'] = last_episode
                        with open('config.ini', 'w') as fichierconfig:
                                config.write(fichierconfig)
                        templateData['message'] = ['serie ' + name + ' mise à jour']
                        return redirect(url_for('main'))
        return render_template('editserie.html', **templateData)

@app.route("/internal/new", methods = ['POST', 'GET'])
def new_entry():
        """page for adding a new show to the list"""
        global templateData
        global config
        if config == None:
                templateData['message'] = ['pas de configuration trouvée']
                return redirect(url_for('edit_config'))
        templateData = {}
        if request.values.get('valider') == 'Valider':
                templateData = {'name' : str(request.values.get('name')).lstrip().rstrip(),
                                'last_episode' : str(request.values.get('last_episode').strip()),
                                'link' : str(request.values.get('link')).strip()}
                if templateData['name'] == '' or templateData['name'] == 'DEFAULT':
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
        global config
        try:
                jd_ip = config['DEFAULT']['jd_ip']
                jd_port = config['DEFAULT']['jd_port']
                host_id = config['DEFAULT']['host_id']
                message = ['config chargée']
        except (KeyError, TypeError):
                config = configparser.ConfigParser()
                jd_ip =''
                jd_port = ''
                host_id = ''
                message = ['config non trouvée']
        templateData = {'jd_ip' : jd_ip, 'jd_port' : jd_port, 'host_id' : host_id, 'message' : message}
        if request.values.get('cancel') == 'Annuler':
                pass
        if request.values.get('valider') == 'Valider':
                jd_ip = str(request.values.get('jd_ip')).strip()
                jd_port = str(request.values.get('jd_port')).strip()
                host_id = str(request.values.get('host_id')).strip()
                if jd_ip == '' or jd_port == '' or host_id == '':
                        templateData['message'] = ['configuration invalide']
                else:
                        config['DEFAULT']['jd_ip'] = jd_ip
                        config['DEFAULT']['jd_port'] = jd_port
                        config['DEFAULT']['host_id'] = host_id
                        config['DEFAULT']['last_episode'] = '0'
                        with open('config.ini', 'w') as fichierconfig:
                                config.write(fichierconfig)
                        templateData['message'] = ['configuration mise à jour']
                        return redirect(url_for('main'))
        return render_template('editconfig.html', **templateData)

if __name__ == "__main__":
        try:
                import webbrowser
                webbrowser.open('http://localhost:8090')
        except ImportError:
                pass
        app.run(host='0.0.0.0', port=8090)

