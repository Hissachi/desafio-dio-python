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


class Banco:
    def __init__(self):
        self._clientes: list[Cliente] = []
        self._contas: list[Conta] = []
        self._agencia = "0001"
        self._numero_conta = 1

    @property
    def clientes(self) -> list[Cliente]:
        return self._clientes

    @property
    def contas(self) -> list[Conta]:
        return self._contas

    @property
    def agencia(self) -> str:
        return self._agencia

    def buscar_cliente(self, cpf: str) -> Cliente | None:
        for cliente in self._clientes:
            if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
                return cliente
        return None

    def criar_cliente(
        self, cpf: str, nome: str, data_nascimento: str, endereco: str
    ) -> Cliente:
        existente = self.buscar_cliente(cpf)
        if existente:
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return existente
        cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
        self._clientes.append(cliente)
        print("=== Usuário criado com sucesso! ===")
        return cliente

    def criar_conta(self, cliente: Cliente) -> Conta:
        conta = ContaCorrente(self._numero_conta, self._agencia, cliente)
        self._contas.append(conta)
        self._numero_conta += 1
        print("\n=== Conta criada com sucesso! ===")
        return conta

    def listar_contas(self) -> None:
        for conta in self._contas:
            titular = conta.cliente
            nome_titular = (
                titular.nome if isinstance(titular, PessoaFisica) else "Unknown"
            )
            print(f"""
===========================================
Agência:\t{conta.agencia}
C/C:\t\t{conta.numero}
Titular:\t{nome_titular}
Saldo:\t\tR$ {conta.saldo:.2f}
===========================================""")


def menu():
    menu = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def main():
    import textwrap

    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do usuário: ")
            cliente = banco.buscar_cliente(cpf)
            if not cliente:
                print("\n@@@ Usuário não encontrado! @@@")
                continue
            if not cliente.contas:
                print("\n@@@ Você precisa cadastrar uma conta primeiro! @@@")
                continue
            valor = float(input("Informe o valor do depósito: "))
            conta = cliente.contas[0]
            conta.depositar(valor)

        elif opcao == "s":
            cpf = input("Informe o CPF do usuário: ")
            cliente = banco.buscar_cliente(cpf)
            if not cliente:
                print("\n@@@ Usuário não encontrado! @@@")
                continue
            if not cliente.contas:
                print("\n@@@ Você precisa cadastrar uma conta primeiro! @@@")
                continue
            valor = float(input("Informe o valor do saque: "))
            conta = cliente.contas[0]
            conta.sacar(valor)

        elif opcao == "e":
            cpf = input("Informe o CPF do usuário: ")
            cliente = banco.buscar_cliente(cpf)
            if not cliente:
                print("\n@@@ Usuário não encontrado! @@@")
                continue
            if not cliente.contas:
                print("\n@@@ Você precisa cadastrar uma conta primeiro! @@@")
                continue
            conta = cliente.contas[0]
            print("\n================ EXTRATO ================")
            transacoes = conta.historico.transacoes
            if not transacoes:
                print("Não foram realizadas movimentações.")
            else:
                for t in transacoes:
                    tipo = "Depósito" if isinstance(t, Deposito) else "Saque"
                    print(f"{tipo}:\tR$ {t.valor:.2f}")
            print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
            print("==========================================")

        elif opcao == "nu":
            cpf = input("Informe o CPF (somente número): ")
            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input(
                "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
            )
            banco.criar_cliente(cpf, nome, data_nascimento, endereco)

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário: ")
            cliente = banco.buscar_cliente(cpf)
            if cliente:
                banco.criar_conta(cliente)
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "lc":
            cpf = input("Informe o CPF do usuário: ")
            cliente = banco.buscar_cliente(cpf)
            if not cliente:
                print("\n@@@ Usuário não encontrado! @@@")
                continue
            if not cliente.contas:
                print("\n@@@ Usuário não possui contas! @@@")
                continue
            for conta in cliente.contas:
                print(f"""
===========================================
Agência:\t{conta.agencia}
C/C:\t\t{conta.numero}
Saldo:\t\tR$ {conta.saldo:.2f}
===========================================""")

        elif opcao == "q":
            break

        else:
            print(
                "Operação inválida, por favor selecione novamente a operação desejada."
            )


if __name__ == "__main__":
    import textwrap

    main()
