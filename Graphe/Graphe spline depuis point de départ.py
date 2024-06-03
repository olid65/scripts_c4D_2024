import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

ROUNDING = 2


def splineFromStartPoint(start_point,dict_from_graph):
    lst_pts = []
    sp = dict_from_graph.get(start_point, None)

    while sp :
        if not sp.GetPointCount() : break

        #si on a déjà des points on ne rajoute pas le premier de la spline
        if lst_pts:
            lst_pts += sp.GetAllPoints()[1:]
        else:
            lst_pts += sp.GetAllPoints()


        start_point = lst_pts[-1]
        start_point = (start_point.x,start_point.z)

        sp = dict_from_graph.get(start_point, None)
    res = c4d.SplineObject(len(lst_pts), c4d.SPLINETYPE_LINEAR)
    res.SetAllPoints(lst_pts)

    #point d'arrivée pour le nom
    last_pt = lst_pts[-1]
    last_pt = (round(last_pt.x,ROUNDING),round(last_pt.z,ROUNDING))
    #res.SetName(f'{round(last_pt.x,ROUNDING)}_{round(last_pt.z,ROUNDING)}')
    res.Message(c4d.MSG_UPDATE)
    return last_pt,res

def getDictFromGraphe(graphe_parent, rounding = ROUNDING):
    """retourne un dictionnaire avec le point de départ (tuple (x,z)) de la spline en key,
       et la spline en valeur"""
    res = {}
    for sp in graphe_parent.GetChildren():
        p = sp.GetPoint(0) * sp.GetMg()
        res[(round(p.x, rounding),round(p.z,rounding))] = sp
    return res
# Main function
def main():
    #on cherche les objets "départs" et "Graphe"
    starts = doc.SearchObject('départs')
    if not starts :
        print('pas de départs')
        return
    graphe_parent = doc.SearchObject('Graphe')

    if not graphe_parent :
        print('pas de Graphe')
        return

    dict_from_graph = getDictFromGraphe(graphe_parent, rounding = 3)
    res = c4d.BaseObject(c4d.Onull)
    res.SetName("Reseau_hydro_sp_completes")
    dic_sp = {}
    for start in starts.GetChildren():
        start_point = start.GetMg().off
        start_point = (start_point.x,start_point.z)
        last_pt,sp = splineFromStartPoint(start_point,dict_from_graph)
        dic_sp.setdefault(last_pt,[]).append(sp)

    #regroupement et colorisation des objets par la position du dernier point
    nb_colors = len(dic_sp.keys())
    intervalle_color = 1./nb_colors

    #couleur de départ en HSV
    color = c4d.Vector(0,1,1)

    for last_pt,lst in dic_sp.items():
        onull = c4d.BaseObject(c4d.Onull)
        onull.SetName(str(last_pt))

        color.x += intervalle_color
        col_RVB = c4d.utils.HSVToRGB(color)
        for sp in lst:
            #couleur par réseau
            sp[c4d.ID_BASEOBJECT_USECOLOR] = c4d.ID_BASEOBJECT_USECOLOR_ALWAYS
            sp[c4d.ID_BASEOBJECT_COLOR] = col_RVB

            #nom = longueur de la spline
            spl = c4d.utils.SplineLengthData()
            spl.Init(sp,0)
            sp.SetName(round(spl.GetLength()))
            sp.InsertUnderLast(onull)
        onull.InsertUnderLast(res)

    doc.StartUndo()
    doc.InsertObject(res)
    doc.AddUndo(c4d.UNDOTYPE_NEW,res)

    doc.EndUndo()
    c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()