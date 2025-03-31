from fasthtml.common import *

def rowButton(accion:str="", url:str="", target:str="", icon:str="", color:str="primary", scroll_to_id:str=None, disabled:bool=False):
    """Creates a common action button with a specific icon and color for table rows."""
    boton = Button(
        cls=f"bg-secondary text-white px-1 mx-1 border border-secondary border-1 rounded" if disabled
        else f"bg-{color} text-white px-1 mx-1 border border-{color} border-1 rounded",
        hx_get=url if url else "#",
        hx_target=f"#{target}" if target else "",
        hx_trigger="click",
        onclick=f"scrollToId('{scroll_to_id}')" if scroll_to_id else "",
        disabled=disabled,
    )(
        I(
            cls=f"{icon} text-black fs-7" if disabled else f"{icon} text-white fs-7",
            title="Not avalaible" if disabled else accion.capitalize(),
            disabled=disabled
        )
    )
    return boton

