from typing import Optional
import c4d
from pathlib import Path

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    
    pth = doc.GetDocumentPath()
    name = doc.GetDocumentName()
    if pth and name:
        path = Path(pth)/name
        c4d.storage.ShowInFinder(path, False)
    else:
        c4d.gui.MessageDialog("Document non enregistré")
"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()