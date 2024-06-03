import c4d
from pathlib import Path
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:

    pth = Path('/Volumes/My Passport Pro/RENDUS_TEMP/PNR_TRIENT/anim_plan_expo_20240320_part2')
    pth = Path('/Volumes/My Passport Pro/RENDUS_TEMP/PNR_TRIENT/anim_plan_expo_20240327')
    #print(pth.stat())
    for fn in pth.glob('*.png'):
        #print(fn.parent)
        #print(fn.name)
        #print(fn.stem)
        #print(fn.stem[:-4])
        #print(fn.stem[-4:])
        
        #je devais rajouter un _ entre date et numerotation 4 chiffres
        new_name = fn.stem[:-4]+'_'+fn.stem[-4:]+fn.suffix
        #print(new_name)
        new_fn = Path(fn.parent/new_name)
        #print(new_fn)
        fn.rename(new_fn)
        continue
        new_no = int(fn.stem[-2:])#+6164
        new_name = fn.stem[:-2]+str(new_no).zfill(4)+fn.suffix
        print(new_name)
        new_fn = Path(fn.parent/new_name)
        fn.rename(new_fn)


if __name__ == '__main__':
    main()