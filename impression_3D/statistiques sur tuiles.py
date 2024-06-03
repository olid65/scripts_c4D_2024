from typing import Optional
import c4d

doc: c4d.documents.BaseDocument  # The active document
op: Optional[c4d.BaseObject]  # The active object, None if unselected

def main() -> None:
    # Called when the plugin is selected by the user. Similar to CommandData.Execute.
    ymin_all = 100000
    ymax_all = 0

    delta_higher = 0
    delta_lower = 100000

    pce_delta_higher = None
    pce_delta_lower = None

    for o in op.GetChildren():
        mg = o.GetMg()
        lst_y = [(p*mg).y for p in o.GetAllPoints()]
        ymin = min(lst_y)
        ymax = max(lst_y)
        delta = ymax-ymin

        if delta>delta_higher:
            delta_higher=delta
            pce_delta_higher = o.GetName()

        if delta< delta_lower:
            delta_lower = delta
            pce_delta_lower = o.GetName()


        if ymin < ymin_all:
            ymin_all = ymin
        if ymax > ymax_all:
            ymax_all = ymax

    print(f'ymin all :      {round(ymin_all,2)}')
    print(f'ymax all :      {round(ymax_all,2)}')
    print(f'delta all :     {round(ymax_all-ymin_all,2)}')
    print(f'delta greater : {round(delta_higher,2)} ({pce_delta_higher})')
    print(f'delta lower :   {round(delta_lower,2)} ({pce_delta_lower})')
    print('-'*50)
    print(round(ymin_all,2))
    print(round(ymax_all,2))
    print(round(ymax_all-ymin_all,2))
    print(round(delta_higher,2))
    print(round(delta_lower,2))

"""
def state():
    # Defines the state of the command in a menu. Similar to CommandData.GetState.
    return c4d.CMD_ENABLED
"""

if __name__ == '__main__':
    main()