from abc import ABC, abstractmethod
from .errores import (
    NoCumpleLongitudMinimaError,
    NoTieneLetraMayusculaError,
    NoTieneLetraMinusculaError,
    NoTieneNumeroError,
    NoTieneCaracterEspecialError,
    NoTienePalabraSecretaError
)

class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        if len(clave) < self._longitud_esperada:
            return False
        return True

    def _contiene_mayuscula(self, clave):
        if not any(c.isupper() for c in clave):
            return False
        return True

    def _contiene_minuscula(self, clave):
        if not any(c.islower() for c in clave):
            return False
        return True

    def _contiene_numero(self, clave):
        if not any(c.isdigit() for c in clave):
            return False
        return True

    @abstractmethod
    def es_valida(self, clave):
        pass

class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(8)

    def contiene_caracter_especial(self, clave):
        especiales = "@_#$%"
        if not any(c in especiales for c in clave):
            return False
        return True

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La clave no cumple con la longitud mínima requerida.")
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError("La clave no contiene ninguna letra mayúscula.")
        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError("La clave no contiene ninguna letra minúscula.")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave no contiene ningún número.")
        if not self.contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError("La clave no contiene ningún caracter especial requerido.")
        return True

class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(6)

    def contiene_calisto(self, clave):
        posicion = clave.lower().find("calisto")
        if posicion == -1:
            return False

        substring = clave[posicion:posicion+7]
        mayusculas = sum(1 for c in substring if c.isupper())

        if mayusculas < 2 or mayusculas == 7:
            return False
        return True

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La clave no cumple con la longitud mínima requerida.")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave no contiene ningún número.")
        if not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError("La clave no contiene la palabra secreta 'calisto' con las condiciones requeridas.")
        return True

class Validador:
    def __init__(self, regla):
        self.regla = regla

    def es_valida(self, clave):
        return self.regla.es_valida(clave)
