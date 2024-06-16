import c4d
import webbrowser
doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    
    url = f'https://smapshot.heig-vd.ch/visit/{op.GetName()}'
    
    webbrowser.open(url)


if __name__ == '__main__':
    main()