from typing import List, Optional

from times import Time, format_time
from utils import leer_int, leer_cadena, crear_menu


class Ficha:

    def __init__(
        self, nombre: str = "", edad: int = 0, nacio: Optional[Time] = None
    ) -> None:

        if nacio is None:
            nacio = Time()
            nacio.set_time(12, 0, 0, "AM")

        self.nombre = nombre
        self.edad = edad
        self.nacio = nacio

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nombre: str) -> None:
        if isinstance(nombre, str):
            self._nombre = nombre
        else:
            raise TypeError("El nombre debe ser una cadena de texto")

    @property
    def edad(self) -> int:
        return self._edad

    @edad.setter
    def edad(self, edad: int) -> None:
        if not isinstance(edad, int) or isinstance(edad, bool):
            raise TypeError("La edad debe ser un numero entero")
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        self._edad = edad

    @property
    def nacio(self) -> Time:
        return self._nacio

    @nacio.setter
    def nacio(self, nacio: Time) -> None:
        if isinstance(nacio, Time):
            self._nacio = nacio
        else:
            raise TypeError("Nacio debe ser Time")

    def visualizar(self) -> None:

        print("Nombre: " + self._nombre)
        print("Edad: " + str(self._edad))
        print("Hora de nacimiento: " + format_time(self._nacio))


class Empleado(Ficha):

    def __init__(
        self,
        nombre: str = "",
        edad: int = 0,
        nacio: Optional[Time] = None,
        categoria: str = "",
        antiguedad: int = 0,
    ) -> None:
        super().__init__(nombre, edad, nacio)
        self.categoria = categoria
        self.antiguedad = antiguedad

    @property
    def categoria(self) -> str:
        """Devuelve la categoría del empleado."""
        return self._categoria

    @categoria.setter
    def categoria(self, categoria: str) -> None:

        if not isinstance(categoria, str):
            raise TypeError("La categoria debe ser una cadena de texto")
        self._categoria = categoria

    @property
    def antiguedad(self) -> int:
        return self._antiguedad

    @antiguedad.setter
    def antiguedad(self, antiguedad: int) -> None:

        if not isinstance(antiguedad, int) or isinstance(antiguedad, bool):
            raise TypeError("La antiguedad debe ser un numero entero")
        if antiguedad < 0:
            raise ValueError("La antiguedad no puede ser negativa")
        self._antiguedad = antiguedad

    def visualizar(self) -> None:
        """Muestra los datos del empleado."""
        super().visualizar()
        print("Categoria: " + self._categoria)
        print("Antiguedad: " + str(self._antiguedad) + " años")


class Cliente(Ficha):

    def __init__(
        self,
        nombre: str = "",
        edad: int = 0,
        nacio: Optional[Time] = None,
        dni: str = "",
    ) -> None:

        super().__init__(nombre, edad, nacio)
        self.dni = dni

    @property
    def dni(self) -> str:
        return self._dni

    @dni.setter
    def dni(self, dni: str) -> None:
        if isinstance(dni, str):
            self._dni = dni
        else:
            raise TypeError("DNI debe ser str")

    def visualizar(self) -> None:

        super().visualizar()
        print("DNI: " + self._dni)

    def __eq__(self, otro: object) -> bool:
        """
        Compara dos clientes basándose en nombre y edad.

        Devuelve:
            True si ambos son clientes con el mismo nombre y la misma edad.
            Si otro no es un Cliente devuelve NotImplemented.
        """
        if not isinstance(otro, Cliente):
            return NotImplemented
        return self.nombre == otro.nombre and self.edad == otro.edad


class RegistroDiario:
    def __init__(self) -> None:
        self._personas: List[Ficha] = []

    @property
    def personas(self) -> List[Ficha]:
        return list(self._personas)

    def agregar_persona(self, persona: Ficha) -> None:
        if not isinstance(persona, (Empleado, Cliente)):
            raise TypeError("Solo se pueden agregar objetos Empleado o Cliente")
        self._personas.append(persona)

    def visualizar_registro(self) -> None:
        if not self._personas:
            print("El registro esta vacio")
            return
        for persona in self._personas:
            persona.visualizar()
            print()

    def visualizar_empleados(self) -> None:
        hay_empleados = False
        for persona in self._personas:
            if self.es_empleado(persona):
                persona.visualizar()
                print()
                hay_empleados = True
        if not hay_empleados:
            print("No hay empleados en el registro")

    @staticmethod
    def es_empleado(persona: Ficha) -> bool:
        return isinstance(persona, Empleado)

    def __getitem__(self, indice: int) -> Ficha:
        return self._personas[indice]

    def __add__(self, otro: "RegistroDiario") -> "RegistroDiario":
        if not isinstance(otro, RegistroDiario):
            return NotImplemented
        combinado = RegistroDiario()
        for persona in self._personas + otro._personas:
            combinado.agregar_persona(persona)
        return combinado


def main() -> None:
    opciones = [
        "Introducir empleado",
        "Introducir cliente",
        "Buscar por nombre (y edad)",
        "Mostrar registro diario",
        "Mostrar empleados",
        "Visualizar persona por indice",
        "Combinar registros diarios",
        "Salir",
    ]

    registro = RegistroDiario()

    while True:
        eleccion = crear_menu(opciones)

        if eleccion == 1:
            nombre = leer_cadena("Nombre: ")
            edad = leer_int("Edad: ")
            nacio = None
            while nacio is None:
                nacio = Time.from_string(
                    leer_cadena("Hora de nacimiento (HH:MM:SS FORMATO): ")
                )
            categoria = leer_cadena("Categoria: ")
            antiguedad = leer_int("Antiguedad (años): ")

            try:
                empleado = Empleado(nombre, edad, nacio, categoria, antiguedad)
                registro.agregar_persona(empleado)
                print("Empleado agregado")
            except (TypeError, ValueError) as error:
                print("Error: " + str(error))

        elif eleccion == 2:
            nombre = leer_cadena("Nombre: ")
            edad = leer_int("Edad: ")
            nacio = None
            while nacio is None:
                nacio = Time.from_string(
                    leer_cadena("Hora de nacimiento (HH:MM:SS FORMATO): ")
                )
            dni = leer_cadena("DNI: ")

            try:
                cliente = Cliente(nombre, edad, nacio, dni)
                registro.agregar_persona(cliente)
                print("Cliente agregado")
            except (TypeError, ValueError) as error:
                print("Error: " + str(error))

        elif eleccion == 3:
            nombre = leer_cadena("Nombre: ")
            edad = leer_int("Edad: ")
            encontrada = False

            for persona in registro.personas:
                if persona.nombre == nombre and persona.edad == edad:
                    if registro.es_empleado(persona):
                        print("Tipo: Empleado")
                    else:
                        print("Tipo: Cliente")
                    persona.visualizar()
                    print()
                    encontrada = True

            if not encontrada:
                print("No se ha encontrado a la persona")

        elif eleccion == 4:
            registro.visualizar_registro()

        elif eleccion == 5:
            registro.visualizar_empleados()

        elif eleccion == 6:
            total = len(registro.personas)
            if total == 0:
                print("El registro esta vacio")
            else:
                indice = leer_int("Indice (0-" + str(total - 1) + "): ")
                if 0 <= indice < total:
                    registro[indice].visualizar()
                else:
                    print("Error: indice fuera de rango")

        elif eleccion == 7:
            otro_registro = RegistroDiario()
            otro_registro.agregar_persona(
                Empleado("Marta", 20, None, "Admin", 3)
            )
            otro_registro.agregar_persona(
                Cliente("Pedro", 40, None, "12345678A88")
            )
            registro = registro + otro_registro
            print("Registros combinados")

        elif eleccion == 8:
            print("Fin del programa")
            break


if __name__ == "__main__":
    main()