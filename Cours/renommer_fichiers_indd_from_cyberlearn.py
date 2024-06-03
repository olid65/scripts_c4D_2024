from typing import Optional
import c4d
from pathlib import Path

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    path = Path('/Users/olivierdonze/Documents/TEMP/20_Outils de représentation graphique-Travail personnel pour lévaluation Indesign-2028616')
    
    for pth in path.glob('*'):
        #print(str(pth.name).split('_')[0])
        
        for fn in pth.rglob('*.indd'):
            #renommer  les fichiers indesign en fonction du nom du dossier
            new_name = str(pth.name).split('_')[0] + str(fn.suffix)
            #print(new_name)
            fn.rename(pth / (str(pth.name).split('_')[0] + str(fn.suffix)))

        

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()