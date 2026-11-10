from typing import List
 
 
def leer_int(mensaje: str = "Entero: ") -> int:
    if not isinstance(mensaje, str):
        raise TypeError("El mensaje debe ser una cadena de texto")
 
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: intente de nuevo")
 
 
def leer_float(mensaje: str = "Coma flotante: ") -> float:
    if not isinstance(mensaje, str):
        raise TypeError("El mensaje debe ser una cadena de texto")
 
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: pon coma flotante")
 
 
def leer_cadena(mensaje: str) -> str:
    if not isinstance(mensaje, str):
        raise TypeError("El mensaje debe ser una cadena de texto")
 
    while True:
        cadena = input(mensaje).strip()
        if cadena:
            return cadena
        print("Error: la cadena no puede estar vacia")
 
 
def crear_menu(opciones: List[str]) -> int:
    if not isinstance(opciones, list) or not all(
        isinstance(opcion, str) for opcion in opciones
    ):
        raise TypeError("Las opciones deben ser una lista de cadenas de texto")
   
 
    for i, opcion in enumerate(opciones):
        print(str(i + 1) + ". " + opcion)
 
    elegir = leer_int()
 
    if elegir <= 0 or elegir > len(opciones):
        print("Error: fuera de rango")
        return crear_menu(opciones)
 
    print("Opcion elegida: " + str(elegir))
    return elegir