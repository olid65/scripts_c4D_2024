import c4d
from math import floor
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.


"""Select MNT"""


ECH = 1000
EPAISSEUR_MIN_EN_MM = 5 
ROUND = 10 #10 arrondi à la dizaine inférieur -> 375.8789 => 370

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    
    alt_min = min([p.y for p in op.GetAllPoints()])
    
    print('alt min : ', alt_min)
    print(f'alt_base => {floor((alt_min-EPAISSEUR_MIN_EN_MM*1000/ECH)/ROUND)*ROUND}')


if __name__ == '__main__':
    main()