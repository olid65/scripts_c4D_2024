from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

#l'élément sélectionné doit contenir les splines rectangle pour regrouper les arbres
#les arbres doivent ^être en enfant de l'élément suivant'

class Tuile(object):
    
     def __init__(self,rectangle):
         self.rect = rectangle
         rad = rectangle.GetRad()
         mp = rectangle.GetRad()
         self.min = c4d.Vector(-rad)
         self.max = c4d.Vector(rad)
     
     def pt_is_inside(self,pt):
         pt = pt*~self.rect.GetMl()
         return pt.x > self.min.x and pt.x < self.max.x and pt.z > self.min.z and pt.z < self.max.z 
     
     def __repr__(self):
         return self.rect.GetName()    

def main() -> None:
    
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    tuiles = [Tuile(o) for o in op.GetChildren()]
    
    trees = op.GetNext().GetChildren()
    
    doc.StartUndo()
    for tree in trees :
        pos = tree.GetMg().off
        for tuile in tuiles:
            if tuile.pt_is_inside(pos):
                clone = tree.GetClone()
                clone.InsertUnderLast(tuile.rect)
                clone.SetMg(c4d.Matrix(tree.GetMg()))
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,clone)

    doc.EndUndo()        
    c4d.EventAdd()    
        

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()