from sqlalchemy import Integer, Boolean, Float

from datetime import datetime
from sqlalchemy import DateTime, Date

def assign_form_data_to_model(model, form_data, exclude_keys=None):
    """
    Assign the form values (form_data) to the SQLAlchemy model,  
    converting the values according to the column type defined in the model.

    Args:
        model: SQLAlchemy model instance (for example, `User`).
        form_data: Dictionary with the form data.
        exclude_keys: List of keys to exclude (for example, ["id"]).
    Returns:
        None
    """
    if exclude_keys is None:
        exclude_keys = []

    for key, value in form_data.items():
        if hasattr(model, key) and key not in exclude_keys:
            column_type = model.__table__.columns[key].type

            # Manejar fechas
            if isinstance(column_type, (DateTime, Date)):
                if not value:
                    setattr(model, key, None)
                else:
                    try:
                        parsed = datetime.strptime(value, "%Y-%m-%d")
                        if isinstance(column_type, Date):
                            parsed = parsed.date()
                        setattr(model, key, parsed)
                    except ValueError:
                        setattr(model, key, None)

            # Handle integers.
            elif isinstance(column_type, Integer):
                setattr(model, key, int(value) if value else None)

            # Handel booleans.
            elif isinstance(column_type, Boolean):
                setattr(model, key, value.lower() == "true" if value else False)

            # Handle floats (numeric & currency columns)
            elif isinstance(column_type, Float):
                if value:
                    # Remove the currency symbol if present and trim spaces.
                    normalized = value.replace("€", "").strip()
                    # If the value contains a comma, it is assumed to be formatted in "de-DE" or "es-ES".
                    if "," in normalized:
                        normalized = normalized.replace(".", "").replace(",", ".")
                    try:
                        setattr(model, key, float(normalized))
                    except ValueError:
                        setattr(model, key, None)
                else:
                    setattr(model, key, None)

            # Other types are assigned directly.
            else:
                setattr(model, key, value)

def model_to_dict(model):
    """
    Convert an SQLAlchemy model into a dictionary, where the keys are the  
    column names and the values are the current values of those columns.
    
    Args:
        model: SQLAlchemy model instance (for example, `User`).

    Returns:
        dict: A dictionary with the model's data.
    """
    result = {}
    for column in model.__table__.columns:
        key = column.name  # Column name
        value = getattr(model, key)  # Column value
        result[key] = value
    return result

def to_dict_list(query_result):
    """Convert a SQLAlchemy query result into a list of dictionaries"""
    return [
        {key: value for key, value in row.__dict__.items() if not key.startswith('_')}
        for row in query_result
    ]

def get_model_columns(model):
    """Get the column names of a SQLAlchemy model."""
    return [column.name for column in model.__table__.columns]

