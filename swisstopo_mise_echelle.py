from typing import Optional
import c4d
from pprint import pprint

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

PLUGIN_ID_SWISSTOPOEXTRACTOR = 1058482


##############################
SCALE_VERT_MNT = 1
SCALE_VERT_BUILDINGS = 1
#################################

NAME_MODEL = "Maquette swisstopo"
NAME_MNT = 'swissalti3d'
NAME_ARBRES = 'Arbres isolés'
NAME_FORETS = 'Forêts'
NAME_POLY_FORET = 'swissalti3d_2m_extrait'
NAME_POINTS_ARBRES_ISOLES = 'arbres_isoles_swisstopo_collets'

NAME_BATI3D = 'swissbuildings3d_v3'

ID_GEOTAG = 1026472

ID_SCALE_MNT = 0
ID_SCALE_BUILDINGS = 1

def searchObjectInHierarchy(obj, name,stop = None):
    """Recherche un objet qui commence par name dans la hiérarchie d'un objet"""
    while obj:
        if name == obj.GetName()[:len(name)]:
            return obj
        res = searchObjectInHierarchy(obj.GetDown(), name,stop = stop)
        if res: return res
        if obj == stop:
            return None
        obj = obj.GetNext()
    return None

def getGeoTags(obj, lst = [],stop = None):
    """Fonction récursive pour rechercher les geotags de la hiérarchie d'un objet"""
    while obj:
        if obj.GetTag(ID_GEOTAG):
            lst.append(obj.GetTag(ID_GEOTAG))
        getGeoTags(obj.GetDown(), lst = lst,stop = stop)
        if obj == stop:
            return lst
        obj = obj.GetNext()
    return lst

def searchCloneurs(obj, lst = [], stop = None):
    while obj:
        if obj.CheckType(c4d.Omgcloner):
            lst.append(obj)
        searchCloneurs(obj.GetDown(), lst = lst, stop = stop)
        if obj == stop : return lst
        obj = obj.GetNext()
    return lst

def getFirstFloor(obj):
    while obj:
        if obj.CheckType(c4d.Ofloor):
            return obj
        res = getFirstFloor(obj.GetDown())
        if res :return res
        obj = obj.GetNext()
    return None



def echelle_maquette(doc) -> None:

    #on récupère l'objet "maquette swisstopo"
    op = doc.SearchObject(NAME_MODEL)
    if not op:
        c4d.gui.MessageDialog(f"""il n'y a pas d'objet nommé "{NAME_MODEL}" """)
        return

    #récupération du basecontainer de l'objet
    #s'il n'existe pas on le crée et on met les échelles à 1
    bc = op[PLUGIN_ID_SWISSTOPOEXTRACTOR]
    if not bc:
        bc = c4d.BaseContainer()
        op[PLUGIN_ID_SWISSTOPOEXTRACTOR] = bc
        #attention de bien laisser un float !
        bc[ID_SCALE_MNT]= float(1)
        bc[ID_SCALE_BUILDINGS]= float(1)

    print(bc[ID_SCALE_MNT],bc[ID_SCALE_BUILDINGS])

    #TODO : faut-il avertir l'utilisateur qu'on efface les tags ?
    lst_geotags = getGeoTags(op,stop = op)
    for tag in lst_geotags:
        tag.Remove()


    #Mise à l'échelle du mnt et des objets points des arbres et forets
    lst_obj_poly = []

    cloners = []

    #on cherche le mnt
    mnt = searchObjectInHierarchy(op, NAME_MNT,stop = op)
    if not mnt :
        c4d.gui.MessageDialog('No mnt found.')
        return

    lst_obj_poly.append(mnt)

    #forêts
    forets =  searchObjectInHierarchy(op, NAME_FORETS,stop = op)

    if forets:
        for o in forets.GetChildren():
            polyobj = searchObjectInHierarchy(o, NAME_POLY_FORET,stop = o)
            if polyobj : lst_obj_poly.append(polyobj)

        #cloners
        cloners_foret = searchCloneurs(forets, lst = [], stop = forets)
        if cloners_foret:
            cloners.extend(cloners_foret)


    #arbres isoles
    isoles = searchObjectInHierarchy(op, NAME_POINTS_ARBRES_ISOLES,stop = op)
    if isoles:
        points_isoles = searchObjectInHierarchy(op, NAME_POINTS_ARBRES_ISOLES,stop = op)
        if points_isoles :
            lst_obj_poly.append(points_isoles)

        cloners_isoles = searchCloneurs(isoles, lst = [], stop = forets)
        if cloners_isoles:
            cloners.extend(cloners_isoles)

    #pprint(lst_obj_poly)
    #print('.'*30)
    #pprint(cloners)


    #############################
    #MISE A L'ECHELLE DU MNT ET DES OBJETS POINTS DES ARBRES ET FORETS
    #############################C
    for obj in lst_obj_poly:
        mg = obj.GetMg()
        #matrice pour enlever l'ancienne échelle (stockée dans le bc)
        m_old_scale = c4d.utils.MatrixScale(c4d.Vector(1,1/bc[ID_SCALE_MNT],1))
        #matrice pour la nouvelle échelle
        m_new_scale =  c4d.utils.MatrixScale(c4d.Vector(1,SCALE_VERT_MNT,1))

        #on multiplie par mg -> monde on multiplie par l'ancienne échelle -> on revient à la normale
        #et on multiplie par la nouvelle, puis inverse mg pour revenir en local (ouf!)
        pts = [p*mg*m_old_scale*m_new_scale*~ mg for p in obj.GetAllPoints()]
        obj.SetAllPoints(pts)
        obj.Message(c4d.MSG_UPDATE)

    ############################
    #MISE A L'ECHELLE DES CLONERS
    ############################
    for cloner in cloners:
        cloner[c4d.ID_MG_TRANSFORM_SCALE,c4d.VECTOR_Y] = SCALE_VERT_BUILDINGS

    ####################
    #MISE A L'ECHELLE DES BATIMENTS
    ####################
    buildings = searchObjectInHierarchy(op, NAME_BATI3D,stop = op)
    if buildings:
        for onull in buildings.GetChildren():
            for o in onull.GetChildren():

                pos = o.GetAbsPos()
                #si l'objet avait déjà une échelle on remet sa pos.y à l'échelle 1
                pos.y/= bc[ID_SCALE_MNT]

                pos.y *= SCALE_VERT_MNT
                o.SetAbsPos(pos)
                scale = o.GetAbsScale()
                scale.y = SCALE_VERT_BUILDINGS
                o.SetAbsScale(scale)
    ###############################
    # FLOOR
    ###############################

    floor = getFirstFloor(doc.GetFirstObject())
    if floor :
        pos = floor.GetAbsPos()
        pos.y/= bc[ID_SCALE_MNT]
        pos.y*= SCALE_VERT_MNT
        floor.SetAbsPos(pos)

    bc[ID_SCALE_MNT]= float(SCALE_VERT_MNT)
    bc[ID_SCALE_BUILDINGS]= float(SCALE_VERT_BUILDINGS)
    op[PLUGIN_ID_SWISSTOPOEXTRACTOR] = bc
    c4d.EventAdd()

    print(bc[ID_SCALE_MNT],bc[ID_SCALE_BUILDINGS])

def main():
    echelle_maquette(doc)


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()