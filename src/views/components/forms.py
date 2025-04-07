"""Components related to Forms"""
from fasthtml.common import *
from src.core.html_wrappers import *
from datetime import date, datetime


def mk_input(id:str="", placeholder:str="", value=None, errors:dict={}, autofocus:bool=False, autocomplete:bool=False, disabled:bool=False, type:str="text", step:str=None, capitalize:bool=False):
    """Function to create <INPUT> in forms"""
    
    input_attrs = dict(
        id=f"{id}",
        name=f'{id}',
        placeholder=placeholder,
        cls='form-control mb-2' if id not in errors else 'form-control border border-danger mb-2',
        autofocus=autofocus,
        autocomplete='off' if not autocomplete else 'on',
        value=value if value else '',
        disabled=disabled,
        type=type,
        oninput="this.value = this.value.toUpperCase()" if capitalize else ""
    )

    if step is not None:
        input_attrs["step"] = step

    return Div(cls='form-floating')(
        Input(**input_attrs),
        Label(placeholder, fr=id),
        Div(id=f"error-{id}", cls="text-danger small mb-3")(errors.get(id, ""))
    )

def mk_select(
    id: str = "",
    placeholder: str = "",
    data_value=None,
    data_dict: dict = None,
    errors: dict = {},
    autofocus: bool = False,
    autocomplete: bool = False,
    disabled=False,
    attrs: dict = {},
    floating: bool = True
):
    """Creates a <SELECT> with or without form-floating and HTMX support"""

    selected_value = str(data_value) if data_value is not None else None

    # Base attributes of the select
    base_attrs = dict(
        id=id,
        name=id,
        aria_label='Floating-label-select',
        cls='form-select mb-2' if id not in errors else 'form-select border border-danger mb-2',
        disabled=disabled,
        autofocus=autofocus,
        autocomplete='off' if not autocomplete else 'on'
    )
    base_attrs.update(attrs)

    select_element = Select(**base_attrs)(
        *[
            Option(value=valor, selected=(str(valor) == selected_value))(texto)
            for valor, texto in (data_dict or {}).items()
        ]
    )

    error_element = Div(id=f"error-{id}", cls="text-danger small mb-3")(errors.get(id, ""))

    if floating:
        return Div(cls='form-floating')(
            select_element,
            Label(placeholder, fr=id),
            error_element
        )
    else:
        return Div()(
            select_element,
            error_element
        )

def mk_textarea(id:str="", form:str="", placeholder:str="", value=None, errors:dict={}, autofocus:bool=False, autocomplete:bool=False, disabled=False):
    """Function to create <TEXTAREA> in forms"""
    
    return Div(cls="form-floating")(
        Textarea(id=f"{id}", disabled=disabled, form=f"{form}", cls="form-control", placeholder=placeholder, rows=f"{len(value.splitlines())+1 if value else '2'}", style="height: auto;")(
            f"{value if value else ''}",
        ),
        Label(fr=f"{id}")(f"{placeholder}"),
        Div(id=f"error-{id}", cls="text-danger small mb-3")(errors[f'{id}'] if f'{id}' in errors else '')
    )

def mk_date(id:str="", placeholder:str="", value=None, errors:dict={}, autofocus:bool=False, disabled=False):
    """Function to create <input type='date'> with error support and correct formatting"""

    # Format if it's datetime or date
    if isinstance(value, (datetime, date)):
        value = value.strftime("%Y-%m-%d")
    elif isinstance(value, str) and len(value) >= 10:
        value = value[:10]  # Trim if it comes as "2025-03-23 00:00:00"

    return Div(cls='form-floating')(
        Input(
            id=id,
            name=id,
            type="date",
            value=value if value else "",
            cls='form-control' if id not in errors else 'form-control border border-danger',
            placeholder=placeholder,
            autofocus=autofocus,
            disabled=disabled
        ),
        Label(placeholder, fr=id),
        Div(id=f"error-{id}", cls="text-danger small mb-3")(errors.get(id, ""))
    )

def mk_number(id: str = "", placeholder: str = "", value=None, errors: dict = {}, autofocus: bool = False, autocomplete: bool = False, disabled=False):
    """Function to create a numeric <INPUT> field that:  
    - Displays the number formatted as "1.234,45" (dot for thousands, comma for decimals).  
    - On focus, removes the separators, converts the value to a plain number with a dot, and selects all content.  
    - On blur, re-formats the number according to the 'de-DE' convention.  
    - Allows only digits and the dot during editing.  
    """
    formatted_value = ""
    if value is not None:
        try:
            num_value = float(value)
            eng_format = f"{num_value:,.2f}"
            # Swap commas and dots to get "1.234,56"
            formatted_value = eng_format.replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            formatted_value = value

    # On focus: remove separators and convert commas to dots, then select all content
    onfocus_js = "this.value = this.value.replace(/\\./g, '').replace(/,/g, '.'); this.select();"
    # Allow only digits and the dot
    onkeypress_js = "if (!/[0-9.]/.test(event.key)) { event.preventDefault(); }"
    # On blur: format the number according to 'de-DE' (European format)
    onblur_js = (
        "var normalized = this.value.replace(/,/g, '.');"
        "var num = parseFloat(normalized);"
        "if (!isNaN(num)) {"
        " this.value = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num);"
        "}"
    )

    return Div(cls='form-floating')(
        Input(
            id=id,
            name=id,
            type="text",  # 'text' is used to allow custom formatting
            placeholder=placeholder,
            cls='form-control mb-2' if id not in errors else 'form-control border border-danger mb-2',
            autofocus=autofocus,
            autocomplete='off' if not autocomplete else 'on',
            value=formatted_value,
            disabled=disabled,
            onfocus=onfocus_js,
            onkeypress=onkeypress_js,
            onblur=onblur_js
        ),
        Label(placeholder, fr=id),
        Div(id=f"error-{id}", cls="text-danger small mb-3")(errors.get(id, ""))
    )

def mk_currency(
    id: str = "",
    placeholder: str = "",
    value=None,
    errors: dict = {},
    autofocus: bool = False,
    autocomplete: bool = False,
    disabled=False,
    cls_extra: str = "",
    floating: bool = True
):
    """Currency (€) numeric field with optional compact format and without floating"""

    # Format the value in Spanish style "1.234,56 €"
    formatted_value = ""
    if value is not None:
        try:
            num_value = float(value)
            eng_format = f"{num_value:,.2f}"
            formatted_value = eng_format.replace(",", "X").replace(".", ",").replace("X", ".") + " €"
        except Exception:
            formatted_value = value

    # JS for formatting.
    onfocus_js = "this.value = this.value.replace(/\\s*€$/, ''); this.value = this.value.replace(/\\./g, '').replace(/,/g, '.'); this.select();"
    onkeypress_js = "if(event.key === '-') { if(this.selectionStart !== 0 || this.value.indexOf('-') !== -1){ event.preventDefault(); }} else if(!/[0-9.]/.test(event.key)) { event.preventDefault(); }"
    onblur_js = (
        "var num = parseFloat(this.value);"
        "if (!isNaN(num)) {"
        " var formatted = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num);"
        " this.value = formatted + ' €';"
        "}"
    )

    # HTML elements.
    input_element = Input(
        id=id,
        name=id,
        type="text",
        placeholder=placeholder,
        cls=f'form-control {cls_extra}' if id not in errors else f'form-control border border-danger {cls_extra}',
        autofocus=autofocus,
        autocomplete='off' if not autocomplete else 'on',
        value=formatted_value,
        disabled=disabled,
        onfocus=onfocus_js,
        onkeypress=onkeypress_js,
        onblur=onblur_js
    )

    error_element = Div(id=f"error-{id}", cls="text-danger small mb-3")(errors.get(id, ""))

    if floating:
        return Div(cls='form-floating')(
            input_element,
            Label(placeholder, fr=id),
            error_element
        )
    else:
        return Div()(
            input_element,
            error_element
        )


