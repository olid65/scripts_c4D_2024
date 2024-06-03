from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

"""Sélectionner les objets parents des bâtiments dont la base doit être remontée
   (chaque batiment doit être un objet séparé !
   au besoin utiliser Tools/Convert/Polygon islands to Objects)"""


# SI DELTA = 3 et ALT = 1 le scripts prend tous les points
# depuis la hauteur minimale +3m et les remonte proportionellement
# pour que les 3m deviennent 1m, les points les plus bas remontent plus
# que les points près de la limite (pas facile à décrire le bouzin !)

DELTA = 3 #-> hauteur pour sélectionner les points depuis la base
ALT = 0.5 #-> hauteur au final en gardant la topologie

def touchMin(poly,obj, miny):
    """renvoie vrai si au moins un des points est un point minimum"""
    a,b,c,d = getPtsPoly(poly,obj)
    return a.y==miny or b.y==miny or c.y==miny

def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    doc.StartUndo()
    for op in doc.GetActiveObjects(0):
        for o in op.GetChildren():
            doc.AddUndo(c4d.UNDOTYPE_CHANGE,o)
            bs = o.GetPointS()
            bs.DeselectAll()
            #on prend le minimum en y pour détecter le plancher
            y = [p.y for p in o.GetAllPoints()]
            miny = min(y)
    
            for i,p in enumerate(o.GetAllPoints()):
                delta = p.y -miny
                if delta<DELTA:
                    p.y = (miny + DELTA) - (1-delta/DELTA)*ALT
                    o.SetPoint(i,p)
                    bs.Select(i)
            o.Message(c4d.MSG_UPDATE)
    doc.EndUndo()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
    c4d.EventAdd()