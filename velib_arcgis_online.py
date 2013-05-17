# -*- coding: cp1252 -*-
# modules Python : requests pour les requêtes HTTP et json pour l'encodage Json
#
import requests, json

# On récupère l'état courant des stations vélib sous forme JSON
# remplacer les "xxx" par votre API Key JC Decaux
#
etat = requests.get('https://api.jcdecaux.com/vls/v1/stations?apiKey=xxxxxxxx&contract=Paris').json()

# d'abord on récupère un Token sur ArcGIS Online qui permettra de s'authentifier sur la plateforme
# Substituer vos propres nom d'utilisateur et mot de passe
#
agol_url = 'https://www.arcgis.com/sharing/rest/generateToken'
agol_user = 'votre_nom_d_utilisateur'
agol_password = 'votre_mot_de_passe'

# Le referer n'a pas d'importance pour ce type de requête à partir d'un script
#
params = {'username': agol_user,'password': agol_password, 'f': 'pjson', 'client': 'referer','referer':'arcgis.com'}
token_reponse = requests.post(agol_url,data=params)
token = token_reponse.json()['token']

# On récupère toutes les stations à partir du service d'entités ArcGIS Online
# en passant le token en paramêtre. Notez le referer passé dans le Header de la requête,
# nécéssaire par rapport à l'encodage du token.
# La requête 1=1 permet de récupérer toutes les stations
# Vous devez changer l'URL d'accés au service d'entités pour pointer vers votre propre service
#
query_url = 'https://services.arcgis.com/xxxxxxxxxxx/ArcGIS/rest/services/xxxxxxx/FeatureServer/0/query'
params = {'where': '1=1','outfields': '*','f': 'json','token': token}
headers = {'referer': 'www.arcgis.com'}
query_reponse = requests.get(query_url,data=params,headers=headers)
features = query_reponse.json()['features']

nb_updated_features=0
nb_unchanged_features=0


updatedFeatures = []

# On itère station par station dans le jeux de données ArcGIS
#
for feature in features:
    number = feature['attributes']['number']
    # On lance la recherche de la station courante dans les données issues de l'API Velib
    #
    for etat_station in etat:
        if etat_station['number'] == number:
            # On a trouvé la station courante,
            # a-t-elle été mise à jour par rapport à son état dans ArcGIS Online ?
            #
            if etat_station['last_update'] > feature['attributes']['last_update']:
                # On met à jour la station (dans les objets Python)
                #
                feature['attributes']['status'] = etat_station['status']
                feature['attributes']['available_bike_stands'] = etat_station['available_bike_stands']
                feature['attributes']['available_bikes'] = etat_station['available_bikes']
                feature['attributes']['last_update'] = etat_station['last_update']
                # On copie la version mise à jour dans une liste des objets mis à jour
                #
                updatedFeatures.append(feature)
                nb_updated_features=nb_updated_features+1
            else:
                nb_unchanged_features=nb_unchanged_features+1
            break

# On va poster via HTTP la liste des objets mis à jour sur le Endpoint REST ArcGIS permettant
# la mise à jour de la couche carto des stations
# Ces objets sont "dumpés" en Json avant d'�tre postés en HTTP
# Vous devez changer l'URL d'accés au service d'entités pour pointer vers votre propre service
#
update_url = 'http://services.arcgis.com/xxxxxxxxxxxxxx/ArcGIS/rest/services/xxxxxxx/FeatureServer/0/updateFeatures'
params = {'features': json.dumps(updatedFeatures),'f': 'json','token': token}
update_reponse = requests.post(update_url,data=params,headers=headers)

print str(nb_updated_features) + " stations mises à jour et " + str(nb_unchanged_features) + ' stations inchangées'
