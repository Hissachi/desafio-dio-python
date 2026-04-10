from datetime import datetime
from abc import ABC, abstractmethod


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @property
    @abstractmethod
    def data(self) -> datetime:
        pass

    @abstractmethod
    def registrar(self, conta: "Conta") -> None:
        pass


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data(self) -> datetime:
        return self._data

    def registrar(self, conta: "Conta") -> None:
        conta.depositar(self.valor)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor
        self._data = datetime.now()

    @property
    def valor(self) -> float:
        return self._valor

    @property
    def data(self) -> datetime:
        return self._data

    def registrar(self, conta: "Conta") -> None:
        conta.sacar(self.valor)
