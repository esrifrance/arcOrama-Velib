arcOrama-Velib
==============

Scripts, code et apps d'intégration des opendata Velib dans ArcGIS

Lien vers l'article arcOrama http://www.arcorama.fr/2013/05/integration-arcgis-opendatavelib-1.html

.....................................
velib_arcgis_online.py
.....................................

Ce script Python permet l'intégration du flux de données temps réel de l'API Velib Opendata dans une classe d'entités stockée sur ArcGIS Online.

La classe d'entités doit déjà contenir 1227 points (à la date de création du script) décrivant les stations avec les champs suivants qui seront mis à jour à chaque exécution :

- number (type: esriFieldTypeInteger, alias: number, SQL Type: sqlTypeOther, nullable: true, editable: true)
- status (type: esriFieldTypeString, alias: status, SQL Type: sqlTypeOther, length: 50, nullable: true, editable: true)
- bike_stands (type: esriFieldTypeSmallInteger, alias: bike_stands, SQL Type: sqlTypeOther, nullable: true, editable: true)
- available_bike_stands (type: esriFieldTypeSmallInteger, alias: available_bike_stands, SQL Type: sqlTypeOther, nullable: true, editable: true)
- available_bikes (type: esriFieldTypeSmallInteger, alias: available_bikes, SQL Type: sqlTypeOther, nullable: true, editable: true)
- last_update (type: esriFieldTypeDate, alias: last_update, SQL Type: sqlTypeOther, length: 8, nullable: true, editable: true)

Vous pouvez créer ce service d'entités en chargeant le fichier stations_velib.csv en suivant la procédure ci-dessous. 

Dans ce script, doivent être modifiés pour correspondre à votre environnement :
- Username/Password ArcGIS Online utilisé pour l'exécution
- URL REST d'accès Query et Update à la classe d'entité des stations

.....................................
stations_velib.csv
.....................................

Ce fichier CSV contient la description des stations et leur positionnement géographique en long/lat et en système de coordonnées Web Mercator (Colonnes X et Y)
Pour créer un service d'entités ArcGIS Online des stations, il faut :
- Si vous désirez, ouvrir le futur service au public, en vous réservant possibilité de mettre à jour via le script Python :
  - Remplacer toutes les occurences de "VotreNom" par votre nom d'utilisateur ArcGIS Online
- Charger le fichier CSV dans votre contenu ArcGIS Online
- Publier un service à partir du fichier CSV
- Si vous désirez, ouvrir le futur service au public, en vous réservant possibilité de mettre à jour via le script Python :
  - Activer le suivi des mises à jour sur le service
  - Réserver la mise à jour des données aux utilisateurs qui les ont créées
  - Ces deux paramètres se configurent en cliquant sur "Modifier" dans les propriétés du service d'entités.
- C'est l'URL REST de ce nouveau service qui devra être utilisé dans le script Python (cf. ci-dessus).

- Dans ce fichier, nous avons supprimé la station 11046 Voltaire, qui n'existe plus et dont les coordonnées fournies par JCDecaux sont 0,0.

- Les données de ce fichiers sont issues du programme OpenData JCDecaux (http://developer.jcdecaux.com) / 2013




