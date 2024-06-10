import c4d
import struct
import json
import os.path
from pathlib import Path

CONTAINER_ORIGIN = 1026473
NB_ALERT = 6

def getCalageFromGeoTif(fn):
    """retourne la valeur du pixel en x et y et la position du coin en haut à gauche en x et y
       attention c'est bien le coin du ratser et pas le centre du pixel
       Ne fonctionne pas avec les rasters tournés, fonctionne bien avec les MNT de l'API REST d'ESRI
       Ne fonctionne pas avec les tuiles du MNT de swisstopo"""

    #voir page 16 pdf description tiff
    #et sur https://docs.python.org/3/library/struct.html pour les codes lettres de struct
    #le nombre en clé représente le type selon description du tif
    # le tuple en valeur représente le nombre d'octets (bytes) et le code utilissé pour unpacker
    # il y en a quelques un dont je ne suis pas sûr !
    dic_types = {1:(1,'x'),
                 2:(1,'c'),
                 3:(2,'h'),
                 4:(4,'l'),
                 5:(8,'ll'),
                 6:(1,'b'),
                 7:(1,'b'),
                 8:(2,'h'),
                 9:(4,'i'),
                 10:(8,'ii'),
                 11:(4,'f'),
                 12:(8,'d'),}

    with open(fn,'rb') as f:
        #le premier byte sert à savoir si on es en bigendian ou pas
        r = f.read(2)
        big = True
        if r == b'II':
            big = False
        if big : big ='>'
        else : big = '<'
        #ensuite on a un nombre de verification ? -> normalement 42  sinon 43 pour les bigTiff
        #le second c'est le début du premier IFD (image file directory) en bytes -> 8 en général (commence à 0)
        s = struct.Struct(f"{big}Hl")
        rec = f.read(6)
        #print(s.unpack(rec))

        #début de l'IFD' normalement commence à 8
        #nombre de tags
        s = struct.Struct(f"{big}H")
        rec = f.read(2)
        nb_tag, = s.unpack(rec)
        dic_tags = {}
        for i in range(nb_tag):
            s = struct.Struct(f"{big}HHlHH")
            rec = f.read(12)
            no,typ,nb,value,xx = s.unpack(rec)
            #print(no,typ,nb,value,xx)
            dic_tags[no] = (typ,nb,value,xx)

        #4 bytes pour si on a plusieurs IFD
        s = struct.Struct(f"{big}l")
        rec = f.read(4)

        #VALEUR DES PIXELS
        t = dic_tags.get(33550,None)
        val_px = []
        if t:
            typ,nb,offset,xx = t
            f.seek(offset)
            nb_bytes,code = dic_types.get(typ,None)
            for i in range(nb):
                s = struct.Struct(f"{big}{code}")
                rec = f.read(nb_bytes)
                [val] = s.unpack(rec)
                val_px.append(val)

        val_px_x,val_px_y,v_z = val_px

        #MATRICE DE CALAGE (coin en bas à gauche)
        t = dic_tags.get(33922,None)
        mat_calage = []
        if t:
            typ,nb,offset,xx = t
            f.seek(offset)
            nb_bytes,code = dic_types.get(typ,None)
            for i in range(nb):
                s = struct.Struct(f"{big}{code}")
                rec = f.read(nb_bytes)
                [val] = s.unpack(rec)
                mat_calage.append(val)
        coord_x = mat_calage[3]
        coord_y = mat_calage[4]

        #PROJECTION (pas utilisée pour l'instant dans la fonction)
        t = dic_tags.get(34737,None)
        if t:
            typ,nb,offset,xx = t
            f.seek(offset)
            nb_bytes,code = dic_types.get(typ,None)
            geoAscii = ''
            for i in range(nb):
                s = struct.Struct(f"{big}{code}")
                rec = f.read(nb_bytes)
                [car] = s.unpack(rec)
                geoAscii+=car.decode('utf-8')

        return val_px_x,val_px_y,coord_x,coord_y


def importGeoTif(fn_tif,doc):
    val_px_x,val_px_y,coord_x,coord_y = getCalageFromGeoTif(fn_tif)
    print(val_px_x,val_px_y,coord_x,coord_y)

    bmp = c4d.bitmaps.BaseBitmap()
    bmp.InitWith(str(fn_tif))

    width, height = bmp.GetSize()
    #print(bmp.GetSize())

    #calcul des coordonnées du centre
    size = c4d.Vector(width*val_px_x,0,-(height*val_px_y))
    centre = c4d.Vector(coord_x,0,coord_y) + size/2
    origine = doc[CONTAINER_ORIGIN]
    if not origine:
        doc[CONTAINER_ORIGIN] = centre
        origine = doc[CONTAINER_ORIGIN]


    bits = bmp.GetBt()
    inc = bmp.GetBt() // 8
    bytesArray = bytearray(inc)
    memoryView = memoryview(bytesArray)
    nb_pts = width*height
    nb_polys = (width-1)*(height-1)
    poly = c4d.PolygonObject(nb_pts,nb_polys)
    #on regarde si la valeur du pixel arrondi au cm
    #est une valeur ronde en m on met la valeur en mètre sinon en cm
    if not round(val_px_x*100)%100:
        poly.SetName(f'{fn_tif.stem}_{round(val_px_x)}m')
    else:
        poly.SetName(f'{fn_tif.stem}_{round(val_px_x*100)}cm')

    pts = []
    polys =[]
    pos = -size/2 + c4d.Vector(val_px_x/2,0,-val_px_y/2)
    #print(pos)
    i = 0
    id_poly =0

    for line in range(height):
        for row in range(width):
            bmp.GetPixelCnt(row, line, 1, memoryView, inc, c4d.COLORMODE_GRAYf, c4d.PIXELCNT_0)
            [y] = struct.unpack('f', bytes(memoryView[0:4]))
            pos.y = y
            pts.append(c4d.Vector(pos))
            pos.x+=val_px_x

            if line >0 and row>0:
                c=i
                b=i-width
                a=b-1
                d = i-1

                poly.SetPolygon(id_poly,c4d.CPolygon(a,b,c,d))
                id_poly+=1

            i+=1

        pos.x = -size.x/2 + val_px_x/2
        pos.z-= val_px_y

    poly.SetAllPoints(pts)
    poly.Message(c4d.MSG_UPDATE)

    doc.InsertObject(poly)
    pos = centre-origine
    poly.SetAbsPos(pos)
    doc.SetActiveObject(poly)


def main():

    path = tif = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY, title="Choose a GeoTif Image directory:")

    if not path : return
    #Si on a plus que 6 tif on demande confirmation
    if len(list(Path(path).rglob('*.tif'))) > NB_ALERT:
        if not c4d.gui.QuestionDialog(f'Are you sure you want to import {len(list(Path(path).rglob("*.tif")))} files ?'):
            return

    for fn_tif in sorted(Path(path).rglob('*.tif'),reverse = True):
        importGeoTif(fn_tif,doc)
    c4d.EventAdd()
    return

if __name__ == '__main__':
    main()