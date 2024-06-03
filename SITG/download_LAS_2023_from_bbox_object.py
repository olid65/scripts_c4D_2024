from typing import Optional
import c4d
import os
from math import floor,ceil

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

CONTAINER_ORIGIN = 1026473

TXT_NOT_SAVED = "Le document doit être enregistré pour pouvoir copier les buildings, vous pourrez le faire à la prochaine étape\nVoulez-vous continuer ?"

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

    return mini, maxi

def get_tiles_within_bounding_box(bounding_box, tile_size=250):
    min_x, min_y, max_x, max_y = bounding_box
    tiles = []

    # Calculer les coordonnées des tuiles touchées
    start_x = (min_x // tile_size) * tile_size
    end_x = (max_x // tile_size) * tile_size
    start_y = (min_y // tile_size) * tile_size
    end_y = (max_y // tile_size) * tile_size

    for x in range(int(start_x), int(end_x) + 1, tile_size):
        for y in range(int(start_y), int(end_y) + 1, tile_size):
            tile_name = f"https://ge.ch/sitg/geodata/SITG/TELECHARGEMENT/LIDAR_2023/{x}_{y}.las.zip"
            print(tile_name)
            tiles.append(tile_name)

    return tiles

def main() -> None:
    if not op :
        print("pas d'objet sélectionné")
        return
    path_doc = doc.GetDocumentPath()

    while not path_doc:
        rep = c4d.gui.QuestionDialog(TXT_NOT_SAVED)
        if not rep : return True
        c4d.documents.SaveDocument(doc, "", c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
        c4d.CallCommand(12098) # Enregistrer le projet
        path_doc = doc.GetDocumentPath()

    pth = os.path.join(path_doc,'photomaillage_SITG')
    #pth = '/Users/olivierdonze/Documents/TEMP/photomaill/test_dwnld'
    if not os.path.isdir(pth):
        os.mkdir(pth)

    origine = doc[CONTAINER_ORIGIN]


    #Si on a un objet sélectionné qui a une géométrie on l'utilise pour la bbox'
    mini,maxi = empriseObject(op, origine)

    xmin,ymin,xmax,ymax = mini.x,mini.z,maxi.x,maxi.z
    bbox = xmin,ymin,xmax,ymax
    #print(xmin,ymin,xmax,ymax)
    x = floor(xmin/250)*250
    y = ceil(ymax/250)*250
    
    #print(x,y)
    #print(xmin,ymin,xmax,ymax)
    
    get_tiles_within_bounding_box(bbox, tile_size=250)
    
    #dans le nom les coordonnées sont le point en bas à gauche
    url = 'https://ge.ch/sitg/geodata/SITG/TELECHARGEMENT/LIDAR_2023/2500250_1119500.las.zip'

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()