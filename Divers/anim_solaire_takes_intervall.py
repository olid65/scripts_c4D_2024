import c4d
from datetime import datetime,timedelta

"""Crée une take par INTERVALLE compris entre DEBUT et FIN
   ATTENTION d'activer' l'AUTOTAKE (Bouton A de la palette take"""

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

DEBUT = '21.03.2024 06:00'
FIN = '21.03.2024 20:00'
INTERVALLE = 2 #nbre heures 
CHECKED = True #pour cocher ou non pour marked render 

dic_mois = {1:'janvier',
            2:'février',
            3:'mars',
            4:'avril',
            5:'mai',
            6:'juin',
            7:'juillet',
            8:'août',
            9:'septembre',
            10:'octobre',
            11:'novembre',
            12:'décembre',}

def get_physical_sky(obj = doc.GetFirstObject()):
    while obj:
        if obj.CheckType(1011146):
            return obj
        
        if get_physical_sky(obj.GetDown()):
            return obj
        obj = obj.GetNext()
    return None
def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    sky = get_physical_sky()
    if not sky :
        sky = c4d.BaseObject(1011146)
        doc.InsertObject(sky)
    #on stocke la valeur de départ du ciel dans un clone
    skyClone = sky.GetClone(c4d.COPYFLAGS_0)    
    # Gets the TakeData from the active document (holds all information about Takes)
    takeData = doc.GetTakeData()
    if takeData is None:
        raise RuntimeError("Failed to retrieve the take data.")
    
    if not takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
        c4d.gui.MessageDialog("Vous devez activer l'Auto Take (bouton A de la palette take)")
        return
        
    # Date et heure de départ
    date_depart = datetime.strptime(DEBUT,"%d.%m.%Y %H:%M")
    
    # Date et heure de fin
    date_fin = datetime.strptime(FIN,"%d.%m.%Y %H:%M")
    
    # Pas d'incrémentation d'une heure
    pas = timedelta(hours=INTERVALLE)
    dtd = c4d.DateTimeData()
    doc.StartUndo()
    # Boucle pour incrémenter d'une heure jusqu'à la date de fin
    while date_depart <= date_fin:       
        dtd.SetDateTime(date_depart)
        # Adds a new Take
        newTake = takeData.AddTake(date_depart.strftime("%d_%m_%Hh%M"), None, None)
        newTake.SetChecked(True)
        if newTake is None:
            raise RuntimeError("Failed to add a new take.")
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ,newTake)
        # Defines the created Take as the active one
        takeData.SetCurrentTake(newTake)
        
    
        # Checks if there is some TakeData and the current mode is set to auto Take
        if takeData and takeData.GetTakeMode() == c4d.TAKE_MODE_AUTO:
            sky[c4d.SKY_DATE_TIME] =dtd
            newTake.AutoTake(takeData, sky, skyClone)
        date_depart += pas
    doc.EndUndo()
    c4d.EventAdd()
    return
    # Parse the time string
    dt = datetime.strptime('16.07.2011 03:37',"%d.%m.%Y %H:%M")
    dtd = c4d.DateTimeData()
    # Fills the Data object with the DateTime object
    dtd.SetDateTime(dt)
    
    t = dtd.GetDateTime()
    print(t.day)
    print(t.month)
    print(t.year)
    sky[c4d.SKY_DATE_TIME] = dtd
    c4d.EventAdd()
if __name__ == '__main__':
    main()