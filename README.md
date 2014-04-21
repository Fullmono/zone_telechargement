zone_telechargement
===================

petit script pour ajouter des liens à jdownloader depuis zone-telechargement

il faut avoir les modules requests et beautifulsoup4 installés

il faut aussi activer le remote control dans jdowndloader

pour avoir accès à la config web, lancer web_interface.py, pour le moment cela est lancé en local sur le port 8090

pour configurer copier le fichier config.ini.example en config.ini et modifier
####config de base
[DEFAULT]
#####IP du serveur jdownloader
jd_ip = localhost
######port pour jdownloader
jd_port = 10025
######de base utiliser 0 comme le dernier épisode téléchargé
last_episode = 0
######provider depuis lequel prendre les liens
host_id = Uptobox

####config de chaque série
#####nom de la série
[name_of_stuff]
#####lien pour la page
link = http://www.zone-telechargement.com/series/vostfr/xxxxx.html
#####dernier épisode téléchargé
last_episode = 12
