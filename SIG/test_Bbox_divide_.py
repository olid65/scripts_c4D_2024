import c4d
from math import ceil
from pathlib import Path
import json
import datetime

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""Recalcule une bbox et calcule la dicision par rapport à un nombre de pixels maximum
   Pratique pour extraire des blocs de MNT/MNS soit pour contourner les limitations des API
   soit pour l'impression 3D avoir directement les blocs à imprimer

   ATTENTION : si on met rajout_demi_px -> True rajoute un demi pixel sur tous les côtés
   pour que les blocs se touchent dans C4D (peux également être fait au moment de l'extraction)
   ATTENTION : Ne pas mettre pour QGIS car les blocs se touchent déjà"""

CONTAINER_ORIGIN = 1026473

def empriseObject(obj, origine):
    geom = obj
    if not geom.CheckType(c4d.Opoint):
        geom = geom.GetCache()
        if not geom : return None
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

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    if op is None:
        c4d.gui.MessageDialog("No object selected")
        return
    #si le document n'est pas géorérférencé on stoppe
    if not doc[CONTAINER_ORIGIN]:
        c4d.gui.MessageDialog("Document not georeferenced")
        return
    bbox = empriseObject(op, doc[CONTAINER_ORIGIN])
    if not bbox:
        c4d.gui.MessageDialog("Object without geometry")
        return
    xmin,ymin,xmax,ymax = empriseObject(op, doc[CONTAINER_ORIGIN])
    # si on n'a pas de largeur ou de hauteur on stoppe
    if (xmax-xmin) < 0.00001 or ymax-ymin < 0.00001:
        c4d.gui.MessageDialog("Object too small")
        return

    pth = Path('/Users/olivierdonze/Documents/TEMP/test_extract_geotif')
    pth.mkdir(exist_ok=True)
    dic_res = {}

    rajout_demi_px = False
    max_px =512
    resol = 2
    dic_res['resolution'] = resol
    #TODO : calculer la bbox depuis l'objet sélectionné ou la vue de haut
    #xmin,ymin,xmax,ymax = 2491608.27245,1119028.7331556678,2498608.27245,1122966.2331556678

    #si on veut obtenir vraiment la taille de la bbox au final on rajoute une demi maill sur tous les côtés
    #xmin,ymin,xmax,ymax = xmin - resol/2, ymin - resol/2, xmax + resol/2, ymax + resol/2
    xcenter = (xmin+xmax)/2
    ycenter = (ymin+ymax)/2
    bbox = f'bbox : {xmin},{ymin},{xmax},{ymax}'
    print(bbox)

    size_x = xmax-xmin
    size_y = ymax-ymin
    px_x = size_x/resol
    px_y = size_y/resol
    print(f'size : {size_x},{size_y}')
    print(f'nb_px : {px_x},{px_y}')

    nb_div_x = ceil(px_x/max_px)
    nb_div_y = ceil(px_y/max_px)
    print(f'nb_div : {nb_div_x}, {nb_div_y}')

    px_part_x = ceil(size_x/nb_div_x/resol)
    px_part_y = ceil(size_y/nb_div_y/resol)

    new_px_x = px_part_x * nb_div_x
    new_size_x = new_px_x * resol


    new_px_y = px_part_y * nb_div_y
    new_size_y = new_px_y * resol

    print(f'new_size : {new_size_x},{new_size_y}')
    print(f'new_nb_px : {new_px_x},{new_px_y}')

    new_xmin = xcenter- new_size_x/2
    new_xmax = xcenter+ new_size_x/2

    new_ymin = ycenter- new_size_y/2
    new_ymax = ycenter+ new_size_y/2


    pos_x = new_xmin
    pos_y = new_ymin
    tile_size_x = px_part_x*resol
    tile_size_y = px_part_y*resol
    i = 1
    #calcul des différentes bbox
    dic_res['bboxes'] = []
    for id_y in range(nb_div_y):
        for id_x in range(nb_div_x):

            #si on rajoute le demi pixel pour des mnt touche touche dans C4D
            #-> je l'ai fait au moment de l'extraction !!!!!!!
            #ATTENTION DE NE PAS LE FAIRE 2x !!!!!!!!!!!
            #ATTENTION Ne pas rajouter pour QGIS !
            if rajout_demi_px:
                bbox_part = pos_x-resol/2,pos_y-resol/2,pos_x+tile_size_x+resol/2,pos_y+tile_size_y+resol/2
            #sinon pour créer des vrt dans QGIS
            else:
                bbox_part = pos_x,pos_y,pos_x+tile_size_x,pos_y+tile_size_y
            #print(f'   {bbox_part},')
            dic_res['bboxes'].append(bbox_part)
            pos_x+=tile_size_x
            i+=1
        pos_x = new_xmin
        pos_y +=tile_size_y

    if rajout_demi_px:
        new_xmin -=  resol/2
        new_ymin -=  resol/2

        new_xmax +=  resol/2
        new_ymax +=  resol/2
    #print(']')
    #new_bbox = f'new_bbox : {new_xmin},{new_ymin},{new_xmax},{new_ymax}'
    #print(new_bbox)


    #écriture du fichier contenant la résolution et les bboxes
    #nom du fichier json contenant la date et l'heure
    fn = pth / f'bbox_{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")}.json'

    with open(fn,'w') as f:
        f.write(json.dumps(dic_res))






if __name__ == '__main__':
    main()