import c4d
from urllib.request import urlopen
from urllib.parse import urlencode
import json
from pathlib import Path

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

URL_BASE = 'https://raster.sitg.ge.ch/arcgis/rest/services'
#URL_BASE = 'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES'

class Bbox:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax


def get_all_services()->list:
    """Get all services from the SITG REST API
    """
    #https://raster.sitg.ge.ch/arcgis/rest/services?f=pjson
    url = URL_BASE + '?f=pjson'
    response = urlopen(url)
    data = json.loads(response.read())
    return data['services']

def get_service_capabilities(service_name:str)->dict:
    """Get capabilities from a service
    """
    #https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer?f=pjson
    url = f"{URL_BASE}/{service_name}/ImageServer?f=pjson"
    response = urlopen(url)
    data = json.loads(response.read())
    return data

def get_all_layers_from_collection_ImageServer(service_name:str,bbox:Bbox=None)->list:
    """Get all layers from a collection ImageServer
    if bbox is not None, return only layers that intersect bbox
    """
    # Construire l'URL pour l'opération query
    query_url = f"{URL_BASE}/{service_name}/ImageServer/query"
    # Paramètres de la requête
    if bbox is None:
        params = {
            'f': 'pjson',  # Format de réponse JSON
            'where': '1=1',  # Clause where pour récupérer tous les enregistrements
            'returnIdsOnly': True  # Retourner seulement les OBJECTID
        }
    else:
        params = {
            'f': 'pjson',  # Format de réponse JSON
            'where': '1=1',  # Clause where pour récupérer tous les enregistrements
            'returnIdsOnly': True,  # Retourner seulement les OBJECTID
            'geometry': f"{bbox.xmin},{bbox.ymin},{bbox.xmax},{bbox.ymax}",
            'geometryType': 'esriGeometryEnvelope',
            'spatialRel': 'esriSpatialRelIntersects'
        }

    # Envoyer la requête
    query_url = query_url + '?' + urlencode(params)
    #print(query_url)
    response = urlopen(query_url)

    # Lire la réponse
    data = response.read().decode('utf-8')

    # si on a une erreur
    if 'error' in data:
        print(query_url)
        print(data)
        return None

    # Convertir la réponse JSON en dictionnaire Python
    data = json.loads(data)

    # Récupérer les OBJECTID
    object_ids = data.get('objectIds', [])

    return object_ids

def get_infos_from_layer_ImageServer(service_name:str,layer_id:str)->dict:
    """Get attributes infos from a layer ImageServer
    """
    # Construire l'URL pour l'opération query
    #https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer/7?f=pjson
    query_url = f"{URL_BASE}/{service_name}/ImageServer/{layer_id}"
    # Paramètres de la requête
    params = {
        'f': 'pjson',  # Format de réponse JSON
    }

    # Envoyer la requête
    query_url = query_url + '?' + urlencode(params)
    #print(query_url)
    response = urlopen(query_url)

    # Lire la réponse
    data = response.read().decode('utf-8')

    # si on a une erreur
    if 'error' in data:
        print(query_url)
        print(data)
        return None

    # Convertir la réponse JSON en dictionnaire Python
    data = json.loads(data)

    return data.get('attributes', [])

def get_catalog_from_collection_ImageServer(service_name:str)->dict:
    """Get catalog from a collection ImageServer
       Get all attributes for all layers
    """
    layers = get_all_layers_from_collection_ImageServer(service_name)
    if layers is None:
        return None
    catalog = {}
    for layer in layers:
        infos = get_infos_from_layer_ImageServer(service_name,str(layer))
        catalog[layer] = infos
    return catalog

def get_image_from_layer_ImageServer(service_name:str,layer_id:str,bbox:Bbox=None)->dict:
    """Get dict for dowonload image and coordinates from a layer ImageServer
    """
    # Construire l'URL pour l'opération query
    #https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer/exportImage
    query_url = f"{URL_BASE}/{service_name}/ImageServer/exportImage"
    # Paramètres de la requête
    params = {
        'f': 'pjson',  # Format de réponse JSON
        'bbox': f"{bbox.xmin},{bbox.ymin},{bbox.xmax},{bbox.ymax}",
        'bboxSR': '2056',
        'imageSR': '2056',
        'size': '1000,1000',
        'format': 'png',
    }

    # Envoyer la requête
    query_url = query_url + '?' + urlencode(params)
    print(query_url)
    #print(query_url)
    response = urlopen(query_url)

    # Lire la réponse
    data = response.read().decode('utf-8')

    # si on a une erreur
    if 'error' in data:
        print(query_url)
        print(data)
        return None

    # Convertir la réponse JSON en dictionnaire Python
    data = json.loads(data)

    return data

def write_json_file(data:dict,filename:str)->None:
    """Write a json file
    """
    #on crée tous les dossiers nécessaires
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    #on écrit le fichier
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    #services = get_all_services()
    #print(services)

    bbox = Bbox(2493788.349003122,1120243.659850257,2494811.1946364124,1121266.5054835472)
    #layers = get_all_layers_from_collection_ImageServer('ORTHOPHOTOS_COLLECTION',bbox = bbox)
    #print(layers)
    #for layer in layers:
        #infos = get_infos_from_layer_ImageServer('ORTHOPHOTOS_COLLECTION',str(layer))
        #print(infos)
        #return
    service_name = 'CARTES_HISTORIQUES_COLLECTION'
    #service_name = 'MNA_TERRAIN_COLLECTION'
    #service_name = 'PLAN_BASE_ARCHIVE_1936_2002'
    #service_name = 'CARTES_DUFOUR_1845_1935'
    #service_name = 'CARTES_SIEGFRIED_1891_1945'

    #catalog = get_catalog_from_collection_ImageServer(service_name)

    #print(get_service_capabilities(service_name))


    #filename = f'/Users/olivierdonze/Documents/TEMP/SITG/{service_name}.json'
    #write_json_file(catalog,filename)

    print(get_image_from_layer_ImageServer(service_name,'1',bbox = bbox))


if __name__ == '__main__':
    main()