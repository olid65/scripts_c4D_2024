import c4d
import sys
from pathlib import Path
import subprocess

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    modulename = 'geopy'

    #valable sur mac -> à adpter sur PC !
    pth_python = Path(sys.prefix)/'python'
    p1 = subprocess.run([pth_python, '-m', 'pip', 'install', modulename], capture_output=True, check=True)
    print(p1.stdout.decode())
    return


    #process = f'"{pth_python}" -m pip install {modulename}'
    #print(process)

    #TODO : vérifier (sur mac en tous cas) si il y a bien dans le sys.path
    # un lien sur /Users/olivierdonze/.local/lib/python3.11/site-packages
    #sinon il faut faire un fichier .pth dans /Users/olivierdonze/Library/Preferences/Maxon/Maxon Cinema 4D 2024_22E620F3/python311/libs

    #on regarde si le module est déjà installé
    try :
        new_module = __import__(modulename)

    #sinon on l'installe
    #TODO : utiliser p
    except:
        #print(f"{modulename} n'est pas installé !")
        p1 = subprocess.run([pth_python, '-m', 'pip', 'install', modulename], capture_output=True, text = True)
        print(p1.stdout)
        return
    print(f'{modulename} est déjà installé !')

    #module_name = 'requests'





if __name__ == '__main__':
    main()