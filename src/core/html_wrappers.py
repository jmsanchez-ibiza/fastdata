# We import fasthtml because we use it as a base.
import fasthtml
# We import configurations.
from src.config import NAVBAR_BG_COLOR

# Our functions are wrappers of those from fasthtml, but using Bootstrap classes and styles.
# We define custom functions to wrap HTML tags with predefined classes and styles.

# Define __all__ to control what gets exported with -> import *
__all__ = ["H1", "P", "Button", "Nav"]

# Dictionary with default configurations for each tag
TAG_DEFAULTS = {
    "Nav": {
        "cls": "navbar navbar-expand-md navbar-light",
        "style": f"background-color: {NAVBAR_BG_COLOR};",
        # "style": f"background-color: {NAVBAR_BG_COLOR}; position: fixed; top: 0; overflow:hidden; width: 100%;"
    },
    "H1": {
        "cls": "fs-1",
        "style": ""
    },
    # Add more default configurations for other tags here...
}


def _custom_tag(tag_func, tag_name, *args, cls="", style="", force_cls: bool = False, force_style: bool = False, **kwargs):
    """
    Generic function to wrap HTML tags with enforced classes and styles.

    - `tag_func`: The original FastHTML function (e.g., fasthtml.common.Nav)  
    - `tag_name`: Manual name of the tag (e.g., "Nav", "H1")  
    - `cls`: Additional custom classes  
    - `style`: Additional custom styles  
    - `force_cls`: If False, the default forced class is not added.  
    - `force_style`: If True, the forced style is added.
    """
    # Gets the default configurations if they exist
    defaults = TAG_DEFAULTS.get(tag_name, {})
    default_cls = defaults.get("cls", "")
    default_style = defaults.get("style", "")

    # We apply force_cls and force_style according to the parameters
    cls = cls if force_cls else f"{cls} {default_cls}".strip()
    style = style if force_style else f"{style} {default_style}".strip()

    return tag_func(*args, cls=cls, style=style, **kwargs)


# Specific functions based on fasthtml using `_custom_tag`
def H1(*args, **kwargs): return _custom_tag(fasthtml.common.H1, "H1", *args, **kwargs)
def P(*args, **kwargs): return _custom_tag(fasthtml.common.P, "P", *args, **kwargs)
def Button(*args, **kwargs): return _custom_tag(fasthtml.common.Button, "Button", *args, **kwargs)
def Nav(*args, **kwargs): return _custom_tag(fasthtml.common.Nav, "Nav", *args, **kwargs)

# Add more functions here...

