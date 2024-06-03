from typing import Optional
import c4d
from pathlib import Path
import filecmp

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def comparer_fichiers(liste_fichiers):
    fichiers_identiques = []

    for i in range(len(liste_fichiers)):
        fichier1 = liste_fichiers[i]

        for j in range(i+1, len(liste_fichiers)):
            fichier2 = liste_fichiers[j]

            if filecmp.cmp(fichier1, fichier2, shallow=False):
                fichiers_identiques.append((fichier1, fichier2))

    return fichiers_identiques

def main() -> None:

    pth = Path('/Users/olivierdonze/Downloads/20_Outils de représentation graphique-Travail personnel pour lévaluation Indesign-2028616')

    liste_fichiers = list(pth.rglob('*.indd'))
    print(f"{len(liste_fichiers)} fichiers trouvés")
    resultat = comparer_fichiers(liste_fichiers)

    if len(resultat) == 0:
        print("Aucun fichier identique trouvé.")
    else:
        print("Fichiers identiques :")
        for fichier1, fichier2 in resultat:
            print(f"- {fichier1} et {fichier2}")

    """
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()