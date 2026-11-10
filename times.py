import re
from typing import Optional


class Time:
    """
    Clase que representa una hora en formato AM/PM o 24 horas.

    Atributos de clase:
        TIME_FORMATS: formatos permitidos ("AM", "PM", "24 HOURS").
        time_count: cuenta el número de objetos Time creados.

    Atributos (privados, expuestos mediante property de solo lectura):
        hours: guarda las horas (1 a 12 en AM/PM, 0 a 23 en 24 HOURS).
        minutes: guarda los minutos (0 a 59).
        seconds: guarda los segundos (0 a 59).
        time_format: guarda el formato: "AM", "PM" o "24 HOURS".
    """

    TIME_FORMATS: tuple[str, ...] = ("AM", "PM", "24 HOURS")
    time_count: int = 0

    def __init__(self) -> None:
        """
        Inicializa los atributos a 0 (hora 00:00:00 en formato "24 HOURS",
        el único formato en el que la hora 0 es válida)
        """
        self.__hours: int = 0
        self.__minutes: int = 0
        self.__seconds: int = 0
        self.__time_format: str = "24 HOURS"
        Time.time_count += 1

    @property
    def hours(self) -> int:
        """Devuelve las horas."""
        return self.__hours

    @property
    def minutes(self) -> int:
        """Devuelve los minutos."""
        return self.__minutes

    @property
    def seconds(self) -> int:
        """Devuelve los segundos."""
        return self.__seconds

    @property
    def time_format(self) -> str:
        """Devuelve el formato de la hora."""
        return self.__time_format

    # Método de instancia: modifica el atributo privado __time_format del
    # objeto, así que necesita acceder a self.
    def __assign_format(self, time_format: str) -> bool:
        """
        Comprueba que time_format tiene un valor correcto y lo asigna al
        atributo correspondiente. Lo convierte a mayúsculas para evitar
        problemas de capitalización.

        Args:
            time_format: cadena con el formato de hora
                ("AM", "PM" o "24 HOURS").

        Devuelve:
            True si el formato es correcto, False en caso contrario.
        """
        if not Time.is_valid_format(time_format):
            return False
        self.__time_format = " ".join(time_format.split()).upper()
        return True

    # Método estático: solo depende del parámetro recibido, no usa self ni
    # atributos de clase.
    @staticmethod
    def __is_24hour_format(time_format: str) -> bool:
        """
        Comprueba si el formato de la hora es "24 HOURS".

        Args:
            time_format: cadena con el formato de hora.

        Devuelve:
            True si formato es "24 HOURS", False en caso contrario.
        """
        return " ".join(time_format.split()).upper() == "24 HOURS"

    # Método estático: valida unos valores candidatos antes de asignarlos,
    # por lo que no depende del estado de ningún objeto ni de la clase.
    @staticmethod
    def _is_valid_time(
        hours: int, minutes: int, seconds: int, time_format: str
    ) -> bool:
        """
        Comprueba si la hora es correcta según el formato.

        Args:
            hours: horas (1 a 12 en AM/PM, 0 a 23 en 24 HOURS).
            minutes: minutos (0 a 59).
            seconds: segundos (0 a 59).
            time_format: formato ("AM", "PM" o "24 HOURS").

        Devuelve:
            True si la hora es correcta, False en caso contrario.
        """
        if not all(isinstance(value, int) for value in (hours, minutes, seconds)):
            return False
        if not Time.is_valid_format(time_format):
            return False
        if Time.__is_24hour_format(time_format):
            valid_hours = 0 <= hours <= 23
        else:
            valid_hours = 1 <= hours <= 12
        return valid_hours and 0 <= minutes <= 59 and 0 <= seconds <= 59

    # Método de instancia: cambia los atributos privados del objeto.
    def set_time(
        self, hours: int, minutes: int, seconds: int, time_format: str
    ) -> bool:
        """
        Asigna una hora.

        Args:
            hours: horas (1 a 12 en AM/PM, 0 a 23 en 24 HOURS).
            minutes: minutos (0 a 59).
            seconds: segundos (0 a 59).
            time_format: formato ("AM", "PM" o "24 HOURS").

        Devuelve:
            True si la hora se pudo asignar correctamente,
            False en caso contrario.
        """
        if not Time._is_valid_time(hours, minutes, seconds, time_format):
            return False
        self.__assign_format(time_format)
        self.__hours = hours
        self.__minutes = minutes
        self.__seconds = seconds
        return True

    # Método de instancia: lee los atributos privados del objeto.
    def get_time(self) -> tuple[int, int, int, str]:
        """
        Devuelve la hora actual del objeto como una tupla
        (horas, minutos, segundos, formato).
        """
        return self.__hours, self.__minutes, self.__seconds, self.__time_format

    # Método de clase: es una factoría que crea instancias, y con cls se crea
    # el objeto de la clase correcta (también si alguien hereda de Time).
    @classmethod
    def from_string(cls, time_string: str) -> Optional["Time"]:
        """
        Crea una nueva instancia de Time a partir de una cadena.

        Args:
            time_string: cadena con la hora en el formato
                "HH:MM:SS FORMATO", donde FORMATO es AM, PM o 24 HOURS.

        Devuelve:
            Una instancia de Time con la hora leída.
            Si la cadena no es válida, muestra un mensaje y devuelve None.
        """
        pattern = r"^(\d{1,2}):(\d{1,2}):(\d{1,2})\s+(AM|PM|24\s+HOURS)$"
        match = re.match(pattern, time_string.strip(), re.IGNORECASE)

        if match is None:
            print("Error: la cadena debe tener el formato HH:MM:SS FORMATO")
            return None

        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        time_format = match.group(4)

        if not cls._is_valid_time(hours, minutes, seconds, time_format):
            print("Error: la hora esta fuera de rango para el formato")
            return None

        new_time = cls()
        new_time.set_time(hours, minutes, seconds, time_format)
        return new_time

    # Método de clase: necesita el atributo de clase TIME_FORMATS, pero no
    # depende de ningún objeto concreto.
    @classmethod
    def is_valid_format(cls, time_format: str) -> bool:
        """
        Comprueba si un formato de hora dado es válido.

        Args:
            time_format: cadena con el formato de hora a comprobar.

        Devuelve:
            True si el formato es válido (AM, PM o 24 HOURS),
            False en caso contrario.
        """
        if not isinstance(time_format, str):
            return False
        return " ".join(time_format.split()).upper() in cls.TIME_FORMATS

    # Método de clase: accede al atributo de clase time_count, que es común a
    # todos los objetos.
    @classmethod
    def get_time_count(cls) -> int:
        """
        Devuelve el número de objetos de la clase que se han creado.

        Devuelve:
            Un número entero de objetos Time creados.
        """
        return cls.time_count


def format_time(time_object: Time) -> str:
    """
    Devuelve la hora de un objeto Time como cadena con formato.

    Args:
        time_object: objeto Time a mostrar.

    Devuelve:
        Cadena con el formato "HH:MM:SS FORMATO".
    """
    hours, minutes, seconds, time_format = time_object.get_time()
    return f"{hours:02d}:{minutes:02d}:{seconds:02d} {time_format}"


def read_int(message: str) -> int:
    """
    Lee un número entero por teclado y repite la petición si no es válido.

    Args:
        message: texto que se muestra al pedir el dato.

    Devuelve:
        El número entero introducido.
    """
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Error: introduzca un numero entero")


def main() -> None:
    """Ejecuta el menú principal del programa."""
    current_time = Time()

    while True:
        print()
        print("1. Introducir una nueva hora")
        print("2. Visualizar hora")
        print("3. Crear una hora a partir de una cadena")
        print("4. Terminar")

        option = read_int("Elija una opcion (1-4): ")

        if option == 1:
            time_format = input("Formato (AM, PM o 24 HOURS): ")
            while not Time.is_valid_format(time_format):
                print("Error: formato no valido")
                time_format = input("Formato (AM, PM o 24 HOURS): ")

            hours = read_int("Horas: ")
            minutes = read_int("Minutos: ")
            seconds = read_int("Segundos: ")

            if current_time.set_time(hours, minutes, seconds, time_format):
                print("Hora asignada correctamente")
            else:
                print("Error: la hora esta fuera de rango para el formato")

        elif option == 2:
            print(format_time(current_time))

        elif option == 3:
            time_string = input("Hora (HH:MM:SS FORMATO): ")
            new_time = Time.from_string(time_string)
            if new_time is not None:
                current_time = new_time
                print("Hora creada: " + format_time(current_time))

        elif option == 4:
            print("Objetos Time creados: " + str(Time.get_time_count()))
            print("Fin del programa")
            break

        else:
            print("Error: opcion fuera de rango")


if __name__ == "__main__":
    main()
