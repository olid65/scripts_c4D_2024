import c4d
from math import ceil

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

"""Recalcule une bbox et calcule la dicision par rapport à un nombre de pixels maximum
   Pratique pour extraire des blocs de MNT/MNS soit pour contourner les limitations des API
   soit pour l'impression 3D avoir directement les blocs à imprimer
   
   ATTENTION : j'ai rajouté un demi pixel de chaque côté car si on importe dans C4D le point est le centre du pixel
   Il fudrait le faire plutôt APRES pour chque tuile si on veut importer directement dans C4D
   mais ne pas le faire si c'est pour créer un rater virtuel QGIS (.vrt)...."""
   
def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    rajout_demi_px = True
    max_px =1024
    resol = 2
    xmin,ymin,xmax,ymax = 2491608.27245,1120949.8900281116,2498566.4166664085,1122966.2331556678
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
    for id_y in range(nb_div_y):
        for id_x in range(nb_div_x):
            
            #si on rajoute le demi pixel pour des mnt touche touche dans C4D
            if rajout_demi_px:
                bbox_part = pos_x- resol/2,pos_y- resol/2,pos_x+tile_size_x+ resol/2,pos_y+tile_size_y+ resol/2
            #sinon pour créer des vrt dans QGIS
            else:
                bbox_part = pos_x,pos_y,pos_x+tile_size_x,pos_y+tile_size_y
            print(f'   pièce n°{i:02d} :{bbox_part}')
            pos_x+=tile_size_x
            i+=1
        pos_x = new_xmin
        pos_y +=tile_size_y
    
    if rajout_demi_px:
        new_xmin -=  resol/2
        new_ymin -=  resol/2
        
        new_xmax +=  resol/2
        new_ymax +=  resol/2
            
    new_bbox = f'new_bbox : {new_xmin},{new_ymin},{new_xmax},{new_ymax}'
    print(new_bbox)
    
   

    


if __name__ == '__main__':
    main()