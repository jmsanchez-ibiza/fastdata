from fasthtml.common import *
from src.core.html_wrappers import *

def error_msg(msg):
    return Div(P(cls="text-danger fw-bold")(msg))

def format_currency(num: float) -> str:
    """
    Converts a float number into a string formatted as currency in the European style,  
    using a period as the thousands separator, a comma as the decimal separator, and adding ' €' at the end.  
  
    Example:
        1253.55 -> "1.253,55 €"
    
    Example of use:
    print(format_currency(1253.55))  # Salida: "1.253,55 €"
    """
    # Format the number in en-US style, which uses commas for thousands and periods for decimals
    eng_format = f"{num:,.2f}"  # ej: "1,253.55"
    # Swap commas and periods to get the European format: "1.253,55"
    formatted = eng_format.replace(",", "X").replace(".", ",").replace("X", ".")
    return formatted + " €"
