from typing import Optional
import c4d
import urllib.parse
import urllib.request
import json

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected


def get_api_info(api_url):
    try:
        # Paramètres de la requête
        params = {'f': 'json'}
        # Encodage des paramètres dans l'URL
        encoded_params = urllib.parse.urlencode(params)
        full_url = f"{api_url}?{encoded_params}"

        # Ouvrir une connexion à l'API
        with urllib.request.urlopen(full_url) as response:
            # Lire les données de l'API
            data = response.read()
            # Charger les données JSON
            api_info = json.loads(data)
            return api_info
    except urllib.error.URLError as e:
        print("Erreur lors de la requête :", e)
        return None



def main() -> None:
    # URL de l'API de géo raster
    url = 'https://raster.sitg.ge.ch/arcgis/rest/services'
    
    # Appel de la fonction pour obtenir les informations de l'API
    api_info = get_api_info(url)
    
    # Vérification si des données ont été récupérées
    if api_info:
        # Affichage des informations de l'API
        #print(json.dumps(api_info, indent=2))  # Afficher joliment les données JSON
        for service in api_info['services']:
            print(service)
    
    
    

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()