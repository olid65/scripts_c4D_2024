from typing import Optional
import c4d
import os
import urllib.request
import json
from pprint import pprint

import socket

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

CONTAINER_ORIGIN = 1026473


"""Il faut avoir dans le presse papier une adresse web de map.geo.admin.ch
   (aller sous partage -> copier le lien)

   Si un objet est sélectionné -> bbox de l'objet
   Sinon -> vue de haut

   L'API Rest de swisstopo est limitée à 201 objets par requête (50 indiquées dans la doc !)
   C'est pour ça qu'il y a une boucle while dans chaque layer
   Il faut vérifier qu'il y a bien toutes les entités car j'ai eu quelques soucis !!!!
   et je ne suis pas certain de mon coup ...

   Enregistre dans un geo json par layer dans un dossier SIG au même endroit que le .c4d"""


def empriseVueHaut(bd, origine):
    dimension = bd.GetFrame()
    largeur = dimension["cr"] - dimension["cl"]
    hauteur = dimension["cb"] - dimension["ct"]

    mini = bd.SW(c4d.Vector(0, hauteur, 0)) + origine
    maxi = bd.SW(c4d.Vector(largeur, 0, 0)) + origine

    return mini.x, mini.z, maxi.x, maxi.z


def empriseObject(obj, origine):
    mg = obj.GetMg()

    rad = obj.GetRad()
    if rad == c4d.Vector(0):
        return 0,0,0,0
    centre = obj.GetMp()

    # 4 points de la bbox selon orientation de l'objet
    pts = [c4d.Vector(centre.x + rad.x, centre.y + rad.y, centre.z + rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y + rad.y, centre.z + rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y - rad.y, centre.z + rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y - rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x + rad.x, centre.y - rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x + rad.x, centre.y + rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y + rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x + rad.x, centre.y - rad.y, centre.z + rad.z) * mg]

    mini = c4d.Vector(min([p.x for p in pts]), min([p.y for p in pts]), min([p.z for p in pts])) + origine
    maxi = c4d.Vector(max([p.x for p in pts]), max([p.y for p in pts]), max([p.z for p in pts])) + origine

    return mini.x, mini.z, maxi.x, maxi.z

def url_swissmap(url):
    """renvoie l'url longue si c'est un raccourci
       l'url si c'est déjà une url longue
       on None si ce n'est pas une url map.geo.admin"""
    pref_courte = 'https://s.geo.admin.ch/'
    len_pref_courte = len(pref_courte)




    if len(url)> len_pref_courte and url[:len_pref_courte] == pref_courte:
        # timeout in seconds
        timeout = 5
        socket.setdefaulttimeout(timeout)

        with urllib.request.urlopen(url) as f:
            url_full = f.geturl()
            return url_full

        return None

    # traitement de l'url
    pref_url_longue = 'https://map.geo.admin.ch/'
    len_pref_url_longue = len(pref_url_longue)

    if len(url)> len_pref_url_longue and url[:len_pref_url_longue] == pref_url_longue:
        return url

    return False

def main() -> None:

    url = c4d.GetStringFromClipboard()
    url_full = url_swissmap(url)

    if not url_full:
        print(f"pas d'url ou url non valide :{url}->{url_full}")
        return
    #url = 'https://s.geo.admin.ch/9a70479efb

    #Geojson files are stored in a 'SIG' directory in the same place that doc
    pth = doc.GetDocumentPath()
    if not pth:
        print('Enregistrez le doc !')
        return
    dirname = 'SIG'
    pth = os.path.join(pth,dirname)

    if not os.path.isdir(pth):
        os.mkdir(pth)

    origin = doc[CONTAINER_ORIGIN]
    if not origin:
        print('doc pas géoréférencé')
        return

    # if an object is selected -> bbox from object
    #else -> TopView
    xmin,ymin,xmax,ymax = 0,0,0,0
    if op:
        xmin,ymin,xmax,ymax = empriseObject(op,origin)

    #si pas d'objet sélectionné, ou pas de géométrie on prend la vue de haut
    if not xmin:
        bd = doc.GetActiveBaseDraw()
        camera = bd.GetSceneCamera(doc)
        if not camera[c4d.CAMERA_PROJECTION] == c4d.Ptop:
            #c4d.gui.MessageDialog(self.TXT_NOT_VIEW_TOP)
            print('pas vue de haut')
            return True
        xmin,ymin,xmax,ymax = empriseVueHaut(bd,origin)

    #xmin,ymin,xmax,ymax = 2502532.5880535203,1135709.8070175762,2510766.2407508674,1140243.9335029575

    # full url from short url
    #with urllib.request.urlopen(url) as f:
        #url_full = f.geturl()
        #print(url_full)

    # get info from full url
    if len(url_full.split('?'))!=2:
        print(f'pb url : {url_full}')
        return
    req = url_full.split('?')[1]
    dico = {}
    for part in req.split('&'):
        key,val = part.split('=')
        if key == 'layers' :
            val = val.split(',')
        elif key == 'layers_opacity':
            val = [float(v) for v in val.split(',')]
        elif key == 'layers_visibility' :
            val = [True if v=='true' else False for v in val.split(',')]
        elif key == 'layers_timestamp':
            # pour les voyages temporels
            #la date est sous la forme 18641231 -> on récupère que l'année
            val = [int(v[:4]) for v in val.split(',') if v]
        elif key in ['E','N','zoom']:
            val = float(val)
        dico[key] = val
    layers = dico['layers']


    for lyr in layers:
        print('-'*20)
        print(lyr)
        #if not visible : continue
        offset = 1
        n = 1
        features = []
        stop = False
        while stop==False:
            fn_geojson = os.path.join(pth,lyr.replace('.','_')+'.geojson')

            url_base = f'https://api3.geo.admin.ch/rest/services/api/MapServer/identify?'
            params = {
                "sr" : "2056",
                "layers":f"all:{lyr}",
                "geometry": f"{xmin},{ymin},{xmax},{ymax}",
                "tolerance":0,
                "lang":'fr',
                "geometryType":"esriGeometryEnvelope",
                "geometryFormat":"geojson",
                "offset":f'{offset-1}',
            }

            query_string = urllib.parse.urlencode( params )
            url = url_base+query_string

            #req = urllib.request.Request(url=url)
            # timeout in seconds
            timeout = 10
            socket.setdefaulttimeout(timeout)

            try:

                with urllib.request.urlopen(url) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    res = data.get('results',None)
                    nb = len(res)
                    print(nb)
                    if not res:
                        stop = True
                    offset+=nb

                    for feat in res:
                        d = {'type':feat['type'],
                             'geometry' :feat['geometry'],
                             'properties' :feat['properties'],
                            }
                        features.append(d)
            except:
                print(url)
                break

            #print(fn_geojson)
            n+=1
            if n>100 :
                print(f"plus de 100 requêtes le fichier {lyr} sera incomplet !")
                break
        #conversion en objet c4d

        dic_geojson = {"type": "FeatureCollection",
                               "features": features,
                               "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::2056" } },}
        with open(fn_geojson,'w',encoding='utf-8') as f:
            f.write(json.dumps(dic_geojson,indent = 4))



"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()