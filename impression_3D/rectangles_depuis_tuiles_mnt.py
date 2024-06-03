from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected



def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    doc.StartUndo()
    for o in doc.GetActiveObjects(0):

        centre = o.GetMp()*o.GetMg()
        rad = o.GetRad()

        rect = c4d.BaseObject(c4d.Osplinerectangle)
        rect.SetName(o.GetName())
        rect.SetAbsPos(centre)
        rect[c4d.PRIM_PLANE] = c4d.PRIM_PLANE_XZ
        rect[c4d.PRIM_RECTANGLE_WIDTH] = rad.x*2
        rect[c4d.PRIM_RECTANGLE_HEIGHT] = rad.z*2
        doc.InsertObject(rect)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,rect)
    doc.EndUndo()
    c4d.EventAdd()


"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()