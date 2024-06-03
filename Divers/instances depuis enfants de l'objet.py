from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    res = c4d.BaseObject(c4d.Onull)
    for o in op.GetChildren():
        inst = c4d.BaseObject(c4d.Oinstance)
        inst.SetName(o.GetName())
        inst[c4d.INSTANCEOBJECT_LINK] = o
        inst.InsertUnderLast(res)
    doc.InsertObject(res)
    c4d.EventAdd()

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()