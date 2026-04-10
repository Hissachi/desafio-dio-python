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


class Historico:
    def __init__(self):
        self._transacoes: list[Transacao] = []

    def adicionar_transacao(self, transacao: Transacao) -> None:
        self._transacoes.append(transacao)

    @property
    def transacoes(self) -> list[Transacao]:
        return self._transacoes


class Conta:
    def __init__(self, numero: int, agencia: str, cliente: "Cliente"):
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._saldo = 0.0
        self._historico = Historico()
        cliente.adicionar_conta(self)

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> "Cliente":
        return self._cliente

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def historico(self) -> Historico:
        return self._historico

    def nova_conta(self, cliente: "Cliente", numero: int, agencia: str) -> "Conta":
        return ContaCorrente(numero, agencia, cliente)

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def sacar(self, valor: float) -> bool:
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False
        if valor > 0:
            self._saldo -= valor
            self._historico.adicionar_transacao(Saque(valor))
            print("\n=== Saque realizado com sucesso! ===")
            return True
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero: int, agencia: str, cliente: "Cliente"):
        super().__init__(numero, agencia, cliente)
        self._limite = 500.0
        self._limite_saques = 3
        self._saques_realizados = 0

    @property
    def limite(self) -> float:
        return self._limite

    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    def sacar(self, valor: float) -> bool:
        excedeu_limite = valor > self._limite
        excedeu_saques = self._saques_realizados >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False
        if excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        if valor > 0:
            self._saldo -= valor
            self._saques_realizados += 1
            self._historico.adicionar_transacao(Saque(valor))
            print("\n=== Saque realizado com sucesso! ===")
            return True
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False


class Cliente:
    def __init__(self, endereco: str):
        self._endereco = endereco
        self._contas: list[Conta] = []

    @property
    def endereco(self) -> str:
        return self._endereco

    @property
    def contas(self) -> list[Conta]:
        return self._contas

    def adicionar_conta(self, conta: Conta) -> None:
        self._contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: str, endereco: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def data_nascimento(self) -> str:
        return self._data_nascimento
