from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

# Sélectionnez le rectangle pour découper les arbres
# attention l'axe doit bien etre dans le sens du rectangle et au centre
# le script cherche points_arbres_SITG_2018 et les tags weights selection de arbres_SITG_2018_cloneur

def main() -> None:
    
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    pts_trees = doc.SearchObject('points_arbres_SITG_2018')
    
    cloner = doc.SearchObject('arbres_SITG_2018_cloneur')
    if not pts_trees or not cloner or not op :
        print('pas ok')
        return
    
    tags = [tag for tag in cloner.GetTags() if tag.CheckType(c4d.Tmgweight)]

    mg = pts_trees.GetMg()
    #bs = pts_trees.GetPointS()
    #bs.DeselectAll()
    ml = op.GetMl()
    rad = op.GetRad()
    
    to_remove = []
    new_pts = []
    for i,pt in enumerate(pts_trees.GetAllPoints()):
        p = pt*mg*~ml
        #print(pt)
        if p.x> rad.x or p.x < -rad.x or p.z > rad.z or p.z < -rad.z:
            #bs.Select(i)
            to_remove.append(i)
        else:
            new_pts.append(pt)
    
    pts_trees.ResizeObject(len(new_pts),0)
    pts_trees.SetAllPoints(new_pts)
    pts_trees.Message(c4d.MSG_UPDATE)
    
    
    for tag in tags:
        weights = c4d.modules.mograph.GeGetMoDataWeights(tag)
        weights = [w for i,w in enumerate(weights) if i not in to_remove]
        c4d.modules.mograph.GeGetMoDataWeights(tag)
        c4d.modules.mograph.GeSetMoDataWeights(tag, weights)
        tag.Message(c4d.MSG_UPDATE)

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()
    c4d.EventAdd()