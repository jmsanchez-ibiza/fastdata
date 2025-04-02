"""Componentes relacionados con los Forms"""
from fasthtml.common import *
from src.core.html_wrappers import *
from datetime import date, datetime


def mk_input_OLD(id:str="", placeholder:str="", value=None, errors:dict={}, autofocus:bool=False, autocomplete:bool=False, disabled=False):
    """Función para crear <INPUT> en los forms"""
    
    return Div(cls='form-floating')(
        Input(id=f"{id}", name=f'{id}', placeholder=placeholder,
            cls='form-control mb-2' if not f'{id}' in errors else 'form-control border border-danger mb-2', autofocus=autofocus, autocomplete='off' if not autocomplete else 'on',
            value=value if value else '',
            disabled=disabled),
        Label(f'{placeholder}', fr=f'{id}'),
        Div(id=f"error-{id}", cls="text-danger small mb-3")(errors[f'{id}'] if f'{id}' in errors else '')
    )

def mk_input(id:str="", placeholder:str="", value=None, errors:dict={}, autofocus:bool=False, autocomplete:bool=False, disabled:bool=False, type:str="text", step:str=None, capitalize:bool=False):
    """Función para crear <INPUT> en los forms"""
    
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

def mk_select_OLD(id:str="", placeholder:str="", data_value=None, data_dict:dict=None, errors:dict={}, autofocus:bool=False, autocomplete:bool=False, disabled=False, attrs: dict = {}):
    """Función para crear <SELECT> en los forms con soporte para HTMX y con valor seleccionado"""

    # Convertir data_value a str para evitar problemas de comparación
    selected_value = str(data_value) if data_value is not None else None

    # Atributos base del <select>
    base_attrs = dict(
        id=id,
        name=id,
        aria_label='Floating label select example',
        cls='form-select mb-2' if id not in errors else 'form-select border border-danger mb-2',
        disabled=disabled,
        autofocus=autofocus,
        autocomplete='off' if not autocomplete else 'on'
    )

    # Atributos adicionales (HTMX, etc.)
    base_attrs.update(attrs)

    return Div(cls='form-floating')(
        Select(**base_attrs)(
            *[
                Option(value=valor, selected=(str(valor) == selected_value))(texto)
                for valor, texto in (data_dict or {}).items()
            ]
        ),
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
    """Crea un <SELECT> con o sin form-floating y soporte HTMX"""

    selected_value = str(data_value) if data_value is not None else None

    # Atributos base del select
    base_attrs = dict(
        id=id,
        name=id,
        aria_label='Floating label select example',
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
    """Función para crear <TEXTAREA> en los forms"""
    
    return Div(cls="form-floating")(
        Textarea(id=f"{id}", disabled=disabled, form=f"{form}", cls="form-control", placeholder=placeholder, rows=f"{len(value.splitlines())+1 if value else '2'}", style="height: auto;")(
            f"{value if value else ''}",
        ),
        Label(fr=f"{id}")(f"{placeholder}"),
        Div(id=f"error-{id}", cls="text-danger small mb-3")(errors[f'{id}'] if f'{id}' in errors else '')
    )

def mk_fecha(id:str="", placeholder:str="", value=None, errors:dict={}, autofocus:bool=False, disabled=False):
    """Función para crear <input type='date'> con soporte de errores y formato correcto"""

    # Formatear si es datetime o date
    if isinstance(value, (datetime, date)):
        value = value.strftime("%Y-%m-%d")
    elif isinstance(value, str) and len(value) >= 10:
        value = value[:10]  # Recorta si viene como "2025-03-23 00:00:00"

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

def mk_numero(id: str = "", placeholder: str = "", value=None, errors: dict = {}, autofocus: bool = False, autocomplete: bool = False, disabled=False):
    """Función para crear un campo <INPUT> numérico que:
       - Muestra el número formateado como "1.234,45" (punto para separar miles y coma para decimales).
       - Al recibir foco, elimina los separadores y convierte el valor a un número simple con punto, y selecciona todo el contenido.
       - Al perder foco, re-formatea el número según la convención 'de-DE'.
       - Solo admite dígitos y el punto en la edición.
    """
    formatted_value = ""
    if value is not None:
        try:
            num_value = float(value)
            eng_format = f"{num_value:,.2f}"
            # Intercambia comas y puntos para obtener "1.234,56"
            formatted_value = eng_format.replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            formatted_value = value

    # Al recibir foco: quitar los separadores y convertir comas a puntos, luego seleccionar todo el contenido
    onfocus_js = "this.value = this.value.replace(/\\./g, '').replace(/,/g, '.'); this.select();"
    # Permitir solo dígitos y el punto
    onkeypress_js = "if (!/[0-9.]/.test(event.key)) { event.preventDefault(); }"
    # Al perder foco: formatear el número según 'de-DE'
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
            type="text",  # Se usa 'text' para permitir el formato personalizado
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

def mk_currency_OLD(id: str = "", placeholder: str = "", value=None, errors: dict = {}, autofocus: bool = False, autocomplete: bool = False, disabled=False):
    """Función para crear un campo numérico de moneda (euros) con:
       - Representación formateada: separador de miles con punto, decimales con coma y el símbolo de € al final.
       - Al recibir foco: se elimina el símbolo y el formato, y se selecciona todo el contenido.
       - Al perder foco: se vuelve a formatear el número y se añade el símbolo de €.
    """
    formatted_value = ""
    if value is not None:
        try:
            num_value = float(value)
            eng_format = f"{num_value:,.2f}"
            formatted_value = eng_format.replace(",", "X").replace(".", ",").replace("X", ".") + " €"
        except Exception:
            formatted_value = value

    onfocus_js = "this.value = this.value.replace(/\\s*€$/, ''); this.value = this.value.replace(/\\./g, '').replace(/,/g, '.'); this.select();"
    onkeypress_js = "if (!/[0-9.]/.test(event.key)) { event.preventDefault(); }"
    onblur_js = (
        "var num = parseFloat(this.value);"
        "if (!isNaN(num)) {"
        " var formatted = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num);"
        " this.value = formatted + ' €';"
        "}"
    )

    return Div(cls='form-floating')(
        Input(
            id=id,
            name=id,
            type="text",
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
    """Campo numérico de moneda (€) con formato opcional compacto y sin floating"""

    # Formatear el valor en formato español "1.234,56 €"
    formatted_value = ""
    if value is not None:
        try:
            num_value = float(value)
            eng_format = f"{num_value:,.2f}"
            formatted_value = eng_format.replace(",", "X").replace(".", ",").replace("X", ".") + " €"
        except Exception:
            formatted_value = value

    # JS para formateo
    onfocus_js = "this.value = this.value.replace(/\\s*€$/, ''); this.value = this.value.replace(/\\./g, '').replace(/,/g, '.'); this.select();"
    onkeypress_js = "if(event.key === '-') { if(this.selectionStart !== 0 || this.value.indexOf('-') !== -1){ event.preventDefault(); }} else if(!/[0-9.]/.test(event.key)) { event.preventDefault(); }"
    onblur_js = (
        "var num = parseFloat(this.value);"
        "if (!isNaN(num)) {"
        " var formatted = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num);"
        " this.value = formatted + ' €';"
        "}"
    )

    # Elementos HTML
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
