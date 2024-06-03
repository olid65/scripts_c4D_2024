import c4d
import random
from math import pi

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """

    for o in op.GetChildren():
        pos = o.GetRelPos()
        pos.z += 25
        o.SetRelPos(pos)

    c4d.EventAdd()

    return
    for o in op.GetChildren():
        rot = o.GetAbsRot()
        rot.x += pi
        o.SetAbsRot(rot)

    c4d.EventAdd()
    return
    srces = op.GetNext().GetChildren()
    random.seed(20)
    for inst in op.GetChildren():
        inst[c4d.INSTANCEOBJECT_LINK]=random.choice(srces)

    c4d.EventAdd()

if __name__ == '__main__':
    main()