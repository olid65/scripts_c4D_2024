import c4d
from pathlib import Path

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    src = Path('/Volumes/My Passport Pro/RENDUS_TEMP/PNR_TRIENT/anim_plan_expo_20240327/anim_plan_expo_202403276790.png')
    
    dbt = 6791
    data = src.read_bytes()
    for i in range(6791,7001):
        name = f'{src.stem[:-4]}{i}{src.suffix}'
        #print(src.name)
        #print(name)
        dest = src.parent/name
        #print(src)
        #print(dest)
        dest.write_bytes(data) #for binary files
    


if __name__ == '__main__':
    main()