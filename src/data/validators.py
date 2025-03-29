"""Functions to validate data"""
import re

def validate_email(email):
    # Regular expression to validate an email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Check if the email matches the regular expression
    if re.match(regex, email):
        return True
    else:
        return False


def validate_nie(nie):
    """
    Validates a NIE (Foreigner Identification Number) in Spain.  
    Format: L-XXXXXXX-Z, where L is a letter (X, Y, Z), X are digits, and Z is a control character.
    """
    nie = nie.upper().replace("-", "").replace(" ", "")
    if not re.match(r'^[XYZ]\d{7}[A-Z]$', nie):
        return False

    # Replace the initial letter (X, Y, Z) with its corresponding numeric value
    letra_inicial = nie[0]
    if letra_inicial == 'X':
        nie = '0' + nie[1:]
    elif letra_inicial == 'Y':
        nie = '1' + nie[1:]
    elif letra_inicial == 'Z':
        nie = '2' + nie[1:]

    # Calculate the control digit
    letras_control = "TRWAGMYFPDXBNJZSQVHLCKE"
    resto = int(nie[:-1]) % 23
    letra_calculada = letras_control[resto]

    return nie[-1] == letra_calculada


def validate_dni(dni):
    """
    Validates a DNI (National Identity Document) in Spain.  
    Format: 8 digits followed by a control letter.
    """
    dni = dni.upper().replace("-", "").replace(" ", "")
    if not re.match(r'^\d{8}[A-Z]$', dni):
        return False

    # Calculate the control letter
    letras_control = "TRWAGMYFPDXBNJZSQVHLCKE"
    resto = int(dni[:-1]) % 23
    letra_calculada = letras_control[resto]

    return dni[-1] == letra_calculada


def validate_cif(cif):
    """
    Validates a CIF (Tax Identification Code) in Spain.  
    Format: A letter (A, B, C, D, E, F, G, H, J, K, L, M, N, P, Q, R, S, U, V, W) followed by 7 digits and a control character (letter or number).
    """
    cif = cif.upper().replace("-", "").replace(" ", "")
    if not re.match(r'^[ABCDEFGHJKLMNPQRSUVW]\d{7}[0-9A-J]$', cif):
        return False

    # Calculate the control digit
    letra = cif[0]
    numeros = cif[1:-1]
    digito_control = cif[-1]

    # Sum of the digits in even and odd positions
    suma_pares = sum(int(n) for n in numeros[1::2])
    suma_impares = sum(sum(divmod(int(n) * 2, 10)) for n in numeros[0::2])
    total = suma_pares + suma_impares

    # Calculate the control digit
    control_calculado = (10 - (total % 10)) % 10

    # If the CIF ends with a letter, it is converted to a number
    if digito_control.isalpha():
        letras_control = "JABCDEFGHI"
        digito_control = letras_control.index(digito_control)

    return str(control_calculado) == str(digito_control)


def validate_nie_dni_cif(documento):
    """
    General function to validate NIE, DNI, or CIF.
    """
    if re.match(r'^[XYZ]', documento):
        return validate_nie(documento)
    elif re.match(r'^\d{8}[A-Z]$', documento):
        return validate_dni(documento)
    elif re.match(r'^[ABCDEFGHJKLMNPQRSUVW]', documento):
        return validate_cif(documento)
    else:
        return False


if __name__ == "__main__":

    # Ejemplos de uso
    print(validate_email("usuario@example.com"))  # True
    print(validate_email("usuario@dominio"))     # False
    print(validate_email("usuario.dominio.com")) # False
    print(validate_email("usuario@dominio."))    # False

    # Ejemplos de uso
    print(validate_nie_dni_cif("X1234567L"))  # True (NIE válido)
    print(validate_nie_dni_cif("12345678Z"))  # True (DNI válido)
    print(validate_nie_dni_cif("A1234567C"))  # True (CIF válido)
    print(validate_nie_dni_cif("X1234567A"))  # False (NIE inválido)
    print(validate_nie_dni_cif("12345678A"))  # False (DNI inválido)
    print(validate_nie_dni_cif("A1234567D"))  # False (CIF inválido)
    print(validate_nie_dni_cif("41448782E"))
    print(validate_nie_dni_cif("B07937238"))
