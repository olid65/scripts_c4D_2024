import c4d,os


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


"""Sélectionner tous les objets que l'on veut en tant que fichier stl indépendant
   Le fichier source doit être enregistré, le script crée des fichiers 
   avec le même nom au même emplacement en rajoutant le nom de chaque objet sélectionné"""


#TODO : vérifier si le fichier existe
#       copier les settings du fichier source (en particulier les unités)
#       vérifier que le fichier source est enregistré sinon demander un nom de et un path de base


# Main function
def main():
    path = doc.GetDocumentPath()
    nom,ext = os.path.splitext(doc.GetDocumentName())

    for o in doc.GetActiveObjects(0):
        name_fn = f'{nom}_{o.GetName()}.stl'
        fn = os.path.join(path,name_fn)
        newdoc = c4d.documents.BaseDocument()

        obj = o.GetClone()
        newdoc.InsertObject(obj)

        c4d.documents.SaveDocument(newdoc, fn, c4d.SAVEDOCUMENTFLAGS_NONE, c4d.FORMAT_STL_EXPORT)

# Execute main()
if __name__=='__main__':
    main()