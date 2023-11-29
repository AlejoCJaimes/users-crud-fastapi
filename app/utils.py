import re
from typing import Tuple, List

def is_password_complex(password: str) -> Tuple[bool, List[str]]:
    
    """
    Verifica si la contraseña cumple con los requisitos de complejidad.
    Devuelve una tupla indicando si la contraseña es compleja y una lista de criterios no cumplidos.
    """
    criteria_not_accepted = []
    # Definir criterios de complejidad de la contraseña
    at_least_one_uppercase = bool(re.search(r"[A-Z]", password))
    at_least_one_lowercase = bool(re.search(r"[a-z]", password))
    at_least_one_digit = bool(re.search(r"\d", password))
    at_least_one_symbol = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    minimum_length = len(password) >= 8  # Ajustar la longitud mínima según sea necesario

    if not at_least_one_uppercase:
        criteria_not_accepted.append("al menos una mayúscula")
    if not at_least_one_lowercase:
        criteria_not_accepted.append("al menos una minúscula")
    if not at_least_one_digit:
        criteria_not_accepted.append("al menos un dígito")
    if not at_least_one_symbol:
        criteria_not_accepted.append("al menos un símbolo")
    if not minimum_length:
        criteria_not_accepted.append("longitud mínima de 8 caracteres")

    # Verificar si se cumplen todos los criterios
    return not criteria_not_accepted, criteria_not_accepted
