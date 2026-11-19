"""Clase abstracta base y entidad Cliente (encapsulación + validaciones)."""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError


class Entidad(ABC):
    """Abstracción general de todo objeto del dominio."""

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible de la entidad."""


class Cliente(Entidad):
    _EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
    _NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,60}$")

    def __init__(self, id_cliente, nombre, email, telefono):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # ---- atributos encapsulados con validación -------------------------
    @property
    def id_cliente(self):
        return self.__id

    @id_cliente.setter
    def id_cliente(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"\d{5,12}", valor.strip()):
            raise ClienteInvalidoError(f"Documento inválido: {valor!r} (5 a 12 dígitos).")
        self.__id = valor.strip()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not self._NOMBRE.match(valor.strip()):
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r} (solo letras, mínimo 3).")
        self.__nombre = valor.strip().title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not self._EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}.")
        self.__email = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"3\d{9}", valor.strip()):
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r} (celular de 10 dígitos que inicia en 3).")
        self.__telefono = valor.strip()

    def describir(self):
        return f"Cliente {self.id_cliente} | {self.nombre} | {self.email} | {self.telefono}"

    def __str__(self):
        return self.describir()
