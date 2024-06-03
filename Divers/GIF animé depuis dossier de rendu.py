from typing import Optional
import c4d
import os
import subprocess
from glob import glob

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

"""Utilise ImageMagick->convert qui doit être installé sous /usr/local/bin/convert
   Le script regarde s'il existe des images au format lister sous exts
   prend la première extension trouvée dans le dossier
   On peurt mettre LOOP à zéro pour des boucles infinies (ils déconseille pour les sites web)
   ou mieux mettre un certain nombre d'itérations
   Si on veut un loop pingpong ( Patrol Cycle) mettre PINGPONG = True"""

#DELAY = 10 # Durée d'animation par image en 1/100e de seconde
LOOP = 30 #nombre de boucle (0=>infini)

PINGPONG = False

def main() -> None:
    rd = doc.GetActiveRenderData()
    #récupération du framerate et conversion en 1/100e de seconde pour le paramètre delay
    delay = 1/rd[c4d.RDATA_FRAMERATE]*400
    #chemin de rendu des images
    fn_dst = rd[c4d.RDATA_PATH]
    if not fn_dst :
        c4d.gui.MessageDialog("Il n'y a pas de chemin de rendu")
        return
    fn_dst = fn_dst+'.gif'
    pth = os.path.dirname(fn_dst)
    exts = ['.jpg','.png']

    ext = None
    for e in exts:
        lst = sorted(glob(os.path.join(pth,'*'+e)))
        if lst:
            ext = e
            break

    if not ext :
        c4d.gui.MessageDialog("Il n'y a pas d'images dans le dossier de rendu, lancez d'abord le rendu en jpg ou png")
        return
    
    if os.path.isfile(fn_dst):
        rep = c4d.gui.QuestionDialog(f"Le fichier {fn_dst} existe déjà, il va être remplacé. Voulez-vous continuer ?")
        if not rep :
            return
    fn_src = os.path.join(pth,f'*{ext}')
    
    if PINGPONG :
        # voir Patrol Cycle dans cette page https://legacy.imagemagick.org/Usage/basics/#duplicate
        # '-duplicate 1,-2-1' -> signifie duppliquer 1fois, la série qui va de l'image -2 (avant-dernière) à l'image 1 (deuxième)
        # on ne dupplique pas la dernière ni la première pour pas qu'elle reste deux fois plus de temps ...
        pingpong = '-duplicate 1,-2-1'
    else :
        pingpong = ''

    cmd = f'/usr/local/bin/convert {pingpong} -delay {delay} -loop {LOOP} {fn_src} {fn_dst}'
    print(cmd)
    out = subprocess.run(cmd, shell=True)
    print(out)





"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()