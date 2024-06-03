from typing import Optional
import c4d
import urllib
import os
from zipfile import ZipFile
import subprocess
from math import floor,ceil

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

CONTAINER_ORIGIN = 1026473

TXT_NOT_SAVED = "Le document doit être enregistré pour pouvoir copier les buildings, vous pourrez le faire à la prochaine étape\nVoulez-vous continuer ?"

def empriseObject(obj, origine):
    geom = obj
    if not geom.CheckType(c4d.Opoint):
        geom = geom.GetCache()
        if not geom.CheckType(c4d.Opoint) : return None
    mg = obj.GetMg()
    pts = [p*mg+origine for p in geom.GetAllPoints()]
    lst_x = [p.x for p in pts]
    lst_y = [p.y for p in pts]
    lst_z = [p.z for p in pts]

    xmin = min(lst_x)
    xmax = max(lst_x)
    ymin = min(lst_y)
    ymax = max(lst_y)
    zmin = min(lst_z)
    zmax = max(lst_z)

    mini = c4d.Vector(xmin,ymin,zmin)
    maxi = c4d.Vector(xmax,ymax,zmax)

    return mini, maxi

def empriseVueHaut(bd, origine):
    dimension = bd.GetFrame()
    largeur = dimension["cr"] - dimension["cl"]
    hauteur = dimension["cb"] - dimension["ct"]

    mini = bd.SW(c4d.Vector(0, hauteur, 0)) + origine
    maxi = bd.SW(c4d.Vector(largeur, 0, 0)) + origine

    return mini, maxi

def main() -> None:
    path_doc = doc.GetDocumentPath()

    while not path_doc:
        rep = c4d.gui.QuestionDialog(TXT_NOT_SAVED)
        if not rep : return True
        c4d.documents.SaveDocument(doc, "", c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
        c4d.CallCommand(12098) # Enregistrer le projet
        path_doc = doc.GetDocumentPath()

    pth = os.path.join(path_doc,'photomaillage_SITG')
    #pth = '/Users/olivierdonze/Documents/TEMP/photomaill/test_dwnld'
    if not os.path.isdir(pth):
        os.mkdir(pth)

    origine = doc[CONTAINER_ORIGIN]


    #Si on a un objet sélectionné qui a une géométrie on l'utilise pour la bbox'
    if op and op.CheckType(c4d.Opoint):
        mini,maxi = empriseObject(op, origine)

    #sinon on prend la vue de haut
    else :
        bd = doc.GetActiveBaseDraw()
        camera = bd.GetSceneCamera(doc)

        if not camera[c4d.CAMERA_PROJECTION] == c4d.Ptop:
            c4d.gui.MessageDialog("Activez une vue de haut")
            return True
        mini, maxi = empriseVueHaut(bd, origine)

    xmin,ymin,xmax,ymax = mini.x,mini.z,maxi.x,maxi.z
    print(xmin,ymin,xmax,ymax)
    x = floor(xmin/100)*100
    y = ceil(ymax/100)*100

    #je prend 1 de sécurité en plus
    #le problème est que les coordonnées de l'objet obj
    #sont un peu décalés par rapport à la géométrie (env 30m en x et en z)
    nb_x = int(ceil((xmax-xmin)/100))+1
    nb_y = int(ceil((ymax-ymin)/100))+1
    for i in range(nb_y):
        for n in range(nb_x):
            #si on a déjà un fichier obj -> on passe
            fn_obj = os.path.join(pth,f'{x}_{y}.obj')
            if os.path.isfile(fn_obj) : continue
            url = f'https://ge.ch/sitg/geodata/SITG/TELECHARGEMENT/PHOTOMESH_3D_2019/{x}_{y}.zip'
            name = url.split('/')[-1]
            fn_dst = os.path.join(pth,name)
            try :
                data = urllib.request.urlopen(url)
            except:
                print(f'problème avec {url}')
                continue

            with open(fn_dst,'wb') as saveFile:
                saveFile.write(data.read())

            #DEZIPPAGE
            with ZipFile(fn_dst, 'r') as zipObj:
                # Extract all the contents of zip file in current directory
                zipObj.extractall(pth)

            #suppression du zip
            os.remove(fn_dst)

            x+=100
        x = floor(xmin/100)*100
        y-=100
    print('ok')

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()