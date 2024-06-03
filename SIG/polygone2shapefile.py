import c4d
import shapefile
import os

# ATTENTION les points des segments doivent être en principe dans le sens horaire
# si on a un TROU, il doivent être antihoraire

# TODO -> détecter ce qui est polygones et trou et vérifier le sens des points

# TODO -> gérer les points intermédiaires selon le type (non linear)
#avec GetCache() -> mais ne supporte pas les segments

CONTAINER_ORIGIN =1026473

def fichierPRJ(fn):
    fn = os.path.splitext(fn)[0]+'.prj'
    f = open(fn,'w')
    f.write("""PROJCS["CH1903+_LV95",GEOGCS["GCS_CH1903+",DATUM["D_CH1903+",SPHEROID["Bessel_1841",6377397.155,299.1528128]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["latitude_of_center",46.95240555555556],PARAMETER["longitude_of_center",7.439583333333333],PARAMETER["azimuth",90],PARAMETER["scale_factor",1],PARAMETER["false_easting",2600000],PARAMETER["false_northing",1200000],UNIT["Meter",1]]""")
    f.close()

def createOutline(sp,distance,doc):

    bc = c4d.BaseContainer()
    bc[c4d.MDATA_SPLINE_OUTLINE] = distance
    bc[c4d.MDATA_SPLINE_OUTLINESEPARATE] = True
    res = c4d.utils.SendModelingCommand(command = c4d.MCOMMAND_SPLINE_CREATEOUTLINE,
                                list = [sp],
                                mode = c4d.MODELINGCOMMANDMODE_ALL,
                                bc = bc,
                                doc = doc)
    if res :
        return res[0]
    else :
        return None

def shapefileFromSpline(sp,doc,fn = None,buffer = 0):
    origine = doc[CONTAINER_ORIGIN]
    if not origine:
        print("pas d'origine")
        return

    if not sp:
        print("pas de spline sélectionnée")
        return

    if not fn :
        fn = c4d.storage.LoadDialog(flags = c4d.FILESELECT_SAVE)
        if not fn : return

    if buffer :
        sp = createOutline(sp,buffer,doc)
        if not sp :
            print("problème outline")
            return
    nb_seg = sp.GetSegmentCount()
    mg = sp.GetMg()
    pts = [p*mg+origine for p in sp.GetAllPoints()]

    #UN SEUL SEGMENT
    if not nb_seg :
        poly = [[[p.x,p.z] for p in pts]]

    #MULTISEGMENT (attention ne foncntionne pas avec segments interne à un autre)
    else:
        poly = []
        id_pt = 0
        for i in range(nb_seg):
            cnt = sp.GetSegment(i)['cnt']
            poly.append([[p.x,p.z] for p in pts[id_pt:id_pt+cnt]])
            id_pt +=cnt

    if not fn : return
    with shapefile.Writer(fn,shapefile.POLYGON) as w:
        w.field('id','I')
        w.record(1)
        w.poly(poly)

        fichierPRJ(fn)

if __name__=='__main__':
    sp = op.GetRealSpline()
    shapefileFromSpline(sp,doc, buffer = 1)