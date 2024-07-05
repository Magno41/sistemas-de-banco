import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    """
    Representa um cliente do banco.

    Atributos:
        endereco (str): Endereço do cliente.
        contas (list): Lista de contas associadas ao cliente.
    """

    def __init__(self, endereco):
        """
        Inicializa um cliente com seu endereço.

        Args:
            endereco (str): Endereço do cliente.
        """
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação em uma conta específica do cliente.

        Args:
            conta (Conta): Conta na qual a transação será realizada.
            transacao (Transacao): Transação a ser realizada.
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma nova conta à lista de contas do cliente.

        Args:
            conta (Conta): Conta a ser adicionada.
        """
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Representa uma pessoa física, que é um tipo de cliente do banco.

    Atributos herdados:
        nome (str): Nome completo da pessoa.
        data_nascimento (str): Data de nascimento da pessoa (formato dd-mm-aaaa).
        cpf (str): CPF da pessoa.
        endereco (str): Endereço da pessoa.
        contas (list): Lista de contas associadas à pessoa.
    """

    def __init__(self, nome, data_nascimento, cpf, endereco):
        """
        Inicializa uma pessoa física com seus dados pessoais.

        Args:
            nome (str): Nome completo da pessoa.
            data_nascimento (str): Data de nascimento da pessoa (formato dd-mm-aaaa).
            cpf (str): CPF da pessoa.
            endereco (str): Endereço da pessoa.
        """
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Representa uma conta bancária genérica.

    Atributos:
        numero (int): Número da conta.
        cliente (Cliente): Cliente associado à conta.
        saldo (float): Saldo atual da conta.
        agencia (str): Agência da conta.
        historico (Historico): Histórico de transações da conta.
    """

    def __init__(self, numero, cliente):
        """
        Inicializa uma conta bancária com número e cliente associado.

        Args:
            numero (int): Número da conta.
            cliente (Cliente): Cliente associado à conta.
        """
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Cria uma nova instância de conta.

        Args:
            cliente (Cliente): Cliente associado à conta.
            numero (int): Número da conta.

        Returns:
            Conta: Nova instância de Conta.
        """
        return cls(numero, cliente)

    @property
    def saldo(self):
        """
        Retorna o saldo atual da conta.

        Returns:
            float: Saldo da conta.
        """
        return self._saldo

    @property
    def numero(self):
        """
        Retorna o número da conta.

        Returns:
            int: Número da conta.
        """
        return self._numero

    @property
    def agencia(self):
        """
        Retorna a agência da conta.

        Returns:
            str: Agência da conta.
        """
        return self._agencia

    @property
    def cliente(self):
        """
        Retorna o cliente associado à conta.

        Returns:
            Cliente: Cliente associado à conta.
        """
        return self._cliente

    @property
    def historico(self):
        """
        Retorna o histórico de transações da conta.

        Returns:
            Historico: Histórico de transações da conta.
        """
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque na conta.

        Args:
            valor (float): Valor a ser sacado.

        Returns:
            bool: True se o saque foi realizado com sucesso, False caso contrário.
        """
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        """
        Realiza um depósito na conta.

        Args:
            valor (float): Valor a ser depositado.

        Returns:
            bool: True se o depósito foi realizado com sucesso, False caso contrário.
        """
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    """
    Representa uma conta corrente, que é um tipo específico de conta bancária.

    Atributos herdados:
        numero (int): Número da conta.
        cliente (Cliente): Cliente associado à conta.
        saldo (float): Saldo atual da conta.
        agencia (str): Agência da conta.
        historico (Historico): Histórico de transações da conta.

    Atributos adicionais:
        limite (float): Limite de saldo negativo permitido.
        limite_saques (int): Número máximo de saques permitidos.
    """

    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        """
        Inicializa uma conta corrente com número, cliente associado, limite de saldo e limite de saques.

        Args:
            numero (int): Número da conta.
            cliente (Cliente): Cliente associado à conta.
            limite (float, optional): Limite de saldo negativo permitido. Padrão é 500.
            limite_saques (int, optional): Número máximo de saques permitidos. Padrão é 3.
        """
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        """
        Realiza um saque na conta corrente, considerando o limite de saldo e número máximo de saques.

        Args:
            valor (float): Valor a ser sacado.

        Returns:
            bool: True se o saque foi realizado com sucesso, False caso contrário.
        """
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        if valor > self._limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite permitido. @@@")
            return False

        numero_saques = len([t for t in self.historico.transacoes if isinstance(t, Saque)])
        if numero_saques >= self._limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        if valor > self.saldo + self._limite:
            print("\n@@@ Operação falhou! Valor do saque excede o limite disponível. @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def __str__(self):
        """
        Retorna uma representação em string da conta corrente.

        Returns:
            str: Representação da conta corrente.
        """
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    """
    Representa o histórico de transações de uma conta bancária.

    Atributos:
        transacoes (list): Lista de transações registradas no histórico.
    """

    def __init__(self):
        """
        Inicializa um histórico de transações vazio.
        """
        self._transacoes = []

    @property
    def transacoes(self):
        """
        Retorna a lista de transações registradas no histórico.

        Returns:
            list: Lista de transações.
        """
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico.

        Args:
            transacao (Transacao): Transação a ser registrada.
        """
        self._transacoes.append({
            "tipo": type(transacao).__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
        })


class Transacao(ABC):
    """
    Classe abstrata para representar uma transação bancária.

    Métodos abstratos:
        valor (property): Retorna o valor da transação.
        registrar(conta): Realiza o registro da transação em uma conta específica.
    """

    @property
    @abstractmethod
    def valor(self):
        """
        Valor da transação (propriedade abstrata).

        Raises:
            NotImplementedError: Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method")

    @abstractmethod
    def registrar(self, conta):
        """
        Registra a transação em uma conta bancária específica (método abstrato).

        Args:
            conta (Conta): Conta bancária na qual a transação será registrada.

        Raises:
            NotImplementedError: Deve ser implementado pelas subclasses.
        """
        raise NotImplementedError("Subclass must implement abstract method")


class Saque(Transacao):
    """
    Representa uma transação de saque bancário.

    Atributos:
        valor (float): Valor do saque.
    """

    def __init__(self, valor):
        """
        Inicializa uma transação de saque com um valor específico.

        Args:
            valor (float): Valor do saque.
        """
        self._valor = valor

    @property
    def valor(self):
        """
        Retorna o valor do saque.

        Returns:
            float: Valor do saque.
        """
        return self._valor

    def registrar(self, conta):
        """
        Registra o saque na conta bancária especificada.

        Args:
            conta (Conta): Conta bancária na qual o saque será registrado.
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Representa uma transação de depósito bancário.

    Atributos:
        valor (float): Valor do depósito.
    """

    def __init__(self, valor):
        """
        Inicializa uma transação de depósito com um valor específico.

        Args:
            valor (float): Valor do depósito.
        """
        self._valor = valor

    @property
    def valor(self):
        """
        Retorna o valor do depósito.

        Returns:
            float: Valor do depósito.
        """
        return self._valor

    def registrar(self, conta):
        """
        Registra o depósito na conta bancária especificada.

        Args:
            conta (Conta): Conta bancária na qual o depósito será registrado.
        """
        conta.historico.adicionar_transacao(self)


def menu():
    """
    Exibe o menu principal do sistema.

    Returns:
        str: Opção selecionada pelo usuário.
    """
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [x]\tSair
    => """
    return input(textwrap.dedent(menu_text))


def filtrar_cliente(cpf, clientes):
    """
    Filtra um cliente pelo CPF na lista de clientes.

    Args:
        cpf (str): CPF do cliente a ser filtrado.
        clientes (list): Lista de clientes.

    Returns:
        Cliente: Cliente encontrado pelo CPF, ou None se não encontrado.
    """
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    """
    Recupera a primeira conta de um cliente.

    Args:
        cliente (Cliente): Cliente para recuperar a conta.

    Returns:
        Conta: Primeira conta encontrada do cliente, ou None se não houver contas.
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    return cliente.contas[0]


def depositar(clientes):
    """
    Realiza o processo de depósito na conta de um cliente.

    Args:
        clientes (list): Lista de clientes para realizar o depósito.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    """
    Realiza o processo de saque na conta de um cliente.

    Args:
        clientes (list): Lista de clientes para realizar o saque.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    """
    Exibe o extrato da conta de um cliente.

    Args:
        clientes (list): Lista de clientes para exibir o extrato.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}")

    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    """
    Cria um novo cliente e o adiciona à lista de clientes.

    Args:
        clientes (list): Lista de clientes para adicionar o novo cliente.
    """
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    """
    Cria uma nova conta para um cliente existente.

    Args:
        numero_conta (int): Número da conta a ser criada.
        clientes (list): Lista de clientes para associar a conta.
        contas (list): Lista de contas para adicionar a nova conta.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    """
    Lista todas as contas bancárias registradas.

    Args:
        contas (list): Lista de contas a serem listadas.
    """
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    """
    Função principal que executa o sistema bancário.
    """
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "x":
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
