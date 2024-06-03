import c4d
from urllib.request import urlopen
from urllib.parse import urlencode
import json
from math import floor

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

URL_BASE = 'https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer/' 

CONTAINER_ORIGIN = 1026473

NB_PIXEL_MAX = 4096/2

def empriseObject(obj, origine):
    geom = obj
    if not geom.CheckType(c4d.Opoint):
        geom = geom.GetCache()
        if not geom.CheckType(c4d.Opoint) : return None
    mg = obj.GetMg()
    pts = [p*mg+origine for p in geom.GetAllPoints()]
    lst_x = [p.x for p in pts]
    lst_y = [p.y for p in pts]
    lst_z = [p.z for p in pts]

    xmin = min(lst_x)
    xmax = max(lst_x)
    ymin = min(lst_y)
    ymax = max(lst_y)
    zmin = min(lst_z)
    zmax = max(lst_z)

    mini = c4d.Vector(xmin,ymin,zmin)
    maxi = c4d.Vector(xmax,ymax,zmax)

    return xmin,zmin,xmax,zmax


def read_json_catalog(fn):
    pass
def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    #emprise de l'objet
    origine_doc = doc[CONTAINER_ORIGIN]
    if not origine_doc:
        c4d.gui.MessageDialog("Il faut un document géoréférencé")
        return

    if not op:
        c4d.gui.MessageDialog("Il faut un objet sélectionné")
        return

    xmin,ymin,xmax,ymax = empriseObject(op,origine_doc)
    width_bbox = xmax-xmin
    height_bbox = ymax-ymin
    paysage = False
    if width_bbox > height_bbox :
        paysage = True
        
    
    epsg = 2056
    #print(xmin,zmin,xmax,zmax)

    # Construire l'URL pour l'opération query
    query_url = f"{URL_BASE}query"
    # Paramètres de la requête
    params = {
        'f': 'pjson',  # Format de réponse JSON
        'where': '1=1',  # Clause where pour récupérer tous les enregistrements
        'returnIdsOnly': True,  # Retourner seulement les OBJECTID
        'geometry': f'{xmin} {ymin} {xmax} {ymax}',
    }

    #url = f'https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer/query?where=1%3D1&objectIds=&time=&geometry={xmin}+{ymin}+{xmax}+{ymax}&geometryType=esriGeometryEnvelope&inSR={epsg}&f=pjson'
    #lecture de l'API REST pour obtenir les layers qui sont touchés par la bbox
    with urlopen(query_url + '?' + urlencode(params)) as response:
        data = json.loads(response.read().decode())
        #si on une erreur on quitte
        if 'error' in data.keys():
            print(data['error']['message'])
            return
        #si on a des résultats on les affiche
        if 'objectIds' in data.keys():
            objectids = data['objectIds']
            print(objectids)
        else:
            print('pas de résultats')
            
    

    fn = '/Users/olivierdonze/Documents/TEMP/SITG_CARTES_HISTORIQUES_COLLECTION.json'
    with open(fn) as f:
        data = json.load(f)
    
    for i in objectids:
        dico = data.get(str(i),None)
        if dico :
            name = dico['Name']
            pxsize = round(dico['pixelSizeX'],2)
            band_cnt = dico['bandCount']
            px_type = dico['pixelType']
            if band_cnt == 1:
                format_img = 'png8'
            else:
                format_img = 'png24'
                
            #calcul de la largeur et hauteur de l'image en pixels
            if paysage:
                width = int(floor(width_bbox/pxsize))
                if width > NB_PIXEL_MAX:
                    width_img = NB_PIXEL_MAX
                else:
                    width_img = width
                
                height_img = int(round((height_bbox/pxsize) * width_img/width))    
                
            else:
                height = int(floor(height_bbox/pxsize))
                if height > NB_PIXEL_MAX:
                    height_img = NB_PIXEL_MAX
                else:
                    height_img = height
                
                width_img = int(round((width_bbox/pxsize) * height_img/height))   
                
            
            #print(width_img,height_img)
            
            
            
            img_url = f'{URL_BASE}{i}/image'
            #https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer/37/image?bbox=2478848.3440000005%2C1106133.9065000005%2C2523631.478100002%2C1138871.9217999987&bboxSR=&size=&imageSR=&format=png24&pixelType=U8&noData=&interpolation=+RSP_BilinearInterpolation&compressionQuality=&bandIds=&f=image
            #https://raster.sitg.ge.ch/arcgis/rest/services/CARTES_HISTORIQUES_COLLECTION/ImageServer/31/image?bbox=2491800.3999073734%2C1117410.55487752%2C2498588.6249855333%2C1122993.40761816&format=png24&pixelType=U8&size=678816%2C4096&f=image
            params ={
                        'bbox': f'{xmin},{ymin},{xmax},{ymax}',
                        'format': f'{format_img}',
                        'pixelType':f'{px_type}',
                        'size': f'{width_img},{height_img}',
                        'f': 'image',  
                        
                    }
            url = img_url + '?' + urlencode(params)
            print(name)
            print(url)
        


if __name__ == '__main__':
    main()