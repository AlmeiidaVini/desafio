menu = """
============ SISTEMA BANCARIO ============
\033[1;36m[1] Registrar Usuario
[2] Cadastrar Conta
[3] Ver Usuarios Cadastrados
[4] Ver Contas Cadastradas
>>>>[5] Deposito
>>>>[6] Saque
>>>>[7] Extrato
[8] Sair\033[0m
Digite a opção desejada: """

# Classe para registrar o histórico das transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Classe Conta Bancaria
class ContaBancaria:
    def __init__(self):
        self.transacoes = []

    def ver_transacoes(self):
        print("\n============ EXTRATO ============")
        if self.transacoes:
            for t in self.transacoes:
                print(t)
        else:
            print("Não há movimentações.")


# Classe Conta Bancária
class Conta:
    def __init__(self, cliente, numero, agencia="001", limite=500.0):
        self.cliente = cliente
        self.numero = numero
        self.agencia = agencia
        self.saldo = 0.0
        self.limite = 500.0
        self.extrato = []
        self.limite = limite
        self.historico = Historico()
        self.numero_saques = 0
        self.LIMITE_SAQUE = 3

    def deposito_fun(self):
        try:
            deposito = float(input("Digite a quantidade de dinheiro que gostaria de depositar: R$ "))
            if deposito > 0:
                self.saldo += deposito
                self.extrato.append(f"\033[32mDepósito: R$ {deposito:.2f}\033[0m")
                print(f"Depósito realizado com sucesso! \033[34mSaldo atual: R$ {self.saldo:.2f}\033[0m")
            else:
                print("O valor do depósito deve ser maior que zero.")
        except ValueError:
            print("Por favor, digite um valor numérico válido.")

    def saque_fun(self):
        try:
            saque = float(input("Digite a quantidade de dinheiro que gostaria de sacar: R$ "))
            if 0 < saque <= self.saldo and self.numero_saques < self.LIMITE_SAQUE and saque <= self.limite:
                self.saldo -= saque
                self.numero_saques += 1
                self.extrato.append(f"\033[31mSaque: R$ {saque:.2f}\033[0m")
                print(f"Saque realizado com sucesso! \033[34mSaldo atual: R$ {self.saldo:.2f}\033[0m")
            elif saque > self.limite:
                print(f"Limite de R${self.limite:.2f} por saque")
            elif self.numero_saques >= self.LIMITE_SAQUE:
                print("Limite de saques diários atingido.")
            elif saque < 0:
                print("O valor do saque deve ser maior que 0")
            else:
                print("Saldo insuficiente.")
        except ValueError:
            print("Por favor, digite um valor numérico válido.")

    def extrato_fun(self):
        print(f"\n============ EXTRATO ============\n")
        if self.extrato:
            for operacao in self.extrato:
                print(operacao)
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.adicionar_transacao(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito realizado com sucesso! Saldo atual: R$ {self.saldo:.2f}")
            return True
        else:
            print("Não há movimentações.")
        print(f"\033[34mSaldo atual: R$ {self.saldo:.2f}\033[0m")
        print("Valor para depósito deve ser maior que zero!")
        return False

    def sacar(self, valor):
        if valor <= 0:
            print("Valor de saque inválido!")
            return False
        elif valor > self.saldo:
            print("Saldo insuficiente!")
            return False
        elif valor > self.limite:
            print(f"O valor excede o limite de saque de R$ {self.limite:.2f}!")
            return False
        elif self.numero_saques >= self.LIMITE_SAQUE:
            print("Limite de saques diários atingido!")
            return False
        else:
            self.saldo -= valor
            self.numero_saques += 1
            self.historico.adicionar_transacao(f"Saque: R$ {valor:.2f}")
            print(f"Saque realizado com sucesso! Saldo atual: R$ {self.saldo:.2f}")
            return True

    def ver_extrato(self):
        self.historico.ver_transacoes()
        print(f"Saldo atual: R$ {self.saldo:.2f}")

    @staticmethod
    def nova_conta(cliente, numero):
        return Conta(cliente, numero)


# Classe Cliente que armazena os dados e suas contas
class Cliente:
    def __init__(self, cpf, nome, nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.nascimento = nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


# Interface Transacao e suas implementações para depósito e saque
class Transacao:
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.sacar(self.valor)


# Classe Cadastramento Bancario
# Classe para gerenciar o cadastramento de usuários e contas
class CadastramentoBancario:
    def __init__(self):
        self.dados_pessoas = []
        self.dados_contas = []
        self.dados_pessoas = []  # Lista de objetos Cliente
        self.dados_contas = []   # Lista de objetos Conta
        self.contador_conta = 1

    def cadastro_user(self):
        cpf = input("Digite o CPF: ")
        for registro in self.dados_pessoas:
            if cpf == registro["cpf"]:
                print("CPF já cadastrado")
        for pessoa in self.dados_pessoas:
            if pessoa.cpf == cpf:
                print("CPF já cadastrado!")
                return
        nome = input("Digite o nome: ")
        nascimento = input("Digite data de nascimento: ")
        endereco = input("Digite seu endereço: ")

        self.dados_pessoas.append({
            "cpf": cpf,
            "nome": nome,
            "nascimento": nascimento,
            "endereco": endereco
        })

        nascimento = input("Digite a data de nascimento: ")
        endereco = input("Digite o endereço: ")
        novo_cliente = Cliente(cpf, nome, nascimento, endereco)
        self.dados_pessoas.append(novo_cliente)
        print("Cadastro concluído com sucesso!")

    def cadastrar_conta(self):
        cpf = input("Digite o CPF do titular da conta: ")

        usuario_encontrado = any(pessoa['cpf'] == cpf for pessoa in self.dados_pessoas)
        if not usuario_encontrado:
            print("Usuário não encontrado. Cadastre o usuário primeiro.")
        cliente_encontrado = None
        for cliente in self.dados_pessoas:
            if cliente.cpf == cpf:
                cliente_encontrado = cliente
                break
        if not cliente_encontrado:
            print("Cliente não encontrado. Realize o cadastro primeiro!")
            return

        nova_conta = {
            "agencia": "001",
            "numero_conta": self.contador_conta,
            "cpf": cpf,
            "conta_bancaria": ContaBancaria()
        }

        nova_conta = Conta(cliente_encontrado, self.contador_conta)
        cliente_encontrado.adicionar_conta(nova_conta)
        self.dados_contas.append(nova_conta)
        print(f"Conta {self.contador_conta} criada com sucesso para CPF {cpf}!")
        print(f"Conta {self.contador_conta} criada com sucesso para {cliente_encontrado.nome}!")
        self.contador_conta += 1

    def ver_pessoas(self):
        if not self.dados_pessoas:
            print("Nenhuma pessoa cadastrada.")
            return

        print("\nPessoas Cadastradas:")
        for pessoa in self.dados_pessoas:
            print(f"CPF: {pessoa['cpf']}, Nome: {pessoa['nome']}, Nascimento: {pessoa['nascimento']}, Endereço: {pessoa['endereco']}")
            print(f"CPF: {pessoa.cpf}, Nome: {pessoa.nome}, Nascimento: {pessoa.nascimento}, Endereço: {pessoa.endereco}")

    def ver_contas(self):
        if not self.dados_contas:
            print("Nenhuma Conta cadastrada.")
            print("Nenhuma conta cadastrada.")
            return

        print("\nContas Cadastradas:")
        for conta in self.dados_contas:
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, CPF: {conta['cpf']}")


# Função principal com o menu do Sistema Bancário
def main():
    menu = """
============ SISTEMA BANCARIO ============
\033[1;36m[1] Registrar Usuario
[2] Cadastrar Conta
[3] Ver Usuarios Cadastrados
[4] Ver Contas Cadastradas
>>>>[5] Deposito
>>>>[6] Saque
>>>>[7] Extrato
[8] Sair\033[0m
Digite a opção desejada: """
    cadastro = CadastramentoBancario()

    while True:
        opcao = input(menu)
        if opcao == "1":
            cadastro.cadastro_user()
        elif opcao == "2":
            cadastro.cadastrar_conta()
        elif opcao == "3":
            cadastro.ver_pessoas()
        elif opcao == "4":
            cadastro.ver_contas()
        elif opcao == "5":
            cpf = input("Digite o CPF do titular: ")
            contas = [conta for conta in cadastro.dados_contas if conta.cliente.cpf == cpf]
            if not contas:
                print("Nenhuma conta encontrada para esse CPF.")
                continue
            print("\nContas disponíveis:")
            for conta in contas:
                print(f"Conta: {conta.numero} | Agência: {conta.agencia}")
            try:
                num = int(input("Digite o número da conta desejada: "))
            except ValueError:
                print("Número de conta inválido!")
                continue
            conta_selecionada = next((c for c in contas if c.numero == num), None)
            if conta_selecionada:
                try:
                    valor = float(input("Digite o valor para depósito: R$ "))
                except ValueError:
                    print("Valor inválido!")
                    continue
                deposito = Deposito(valor)
                deposito.registrar(conta_selecionada)
            else:
                print("Conta não encontrada.")
        elif opcao == "6":
            cpf = input("Digite o CPF do titular: ")
            contas = [conta for conta in cadastro.dados_contas if conta.cliente.cpf == cpf]
            if not contas:
                print("Nenhuma conta encontrada para esse CPF.")
                continue
            print("\nContas disponíveis:")
            for conta in contas:
                print(f"Conta: {conta.numero} | Agência: {conta.agencia}")
            try:
                num = int(input("Digite o número da conta desejada: "))
            except ValueError:
                print("Número de conta inválido!")
                continue
            conta_selecionada = next((c for c in contas if c.numero == num), None)
            if conta_selecionada:
                try:
                    valor = float(input("Digite o valor para saque: R$ "))
                except ValueError:
                    print("Valor inválido!")
                    continue
                saque = Saque(valor)
                saque.registrar(conta_selecionada)
            else:
                print("Conta não encontrada.")
        elif opcao == "7":
            cpf = input("Digite o CPF do titular: ")
            contas = [conta for conta in cadastro.dados_contas if conta.cliente.cpf == cpf]
            if not contas:
                print("Nenhuma conta encontrada para esse CPF.")
                continue
            print("\nContas disponíveis:")
            for conta in contas:
                print(f"Conta: {conta.numero} | Agência: {conta.agencia}")
            try:
                num = int(input("Digite o número da conta desejada: "))
            except ValueError:
                print("Número de conta inválido!")
                continue
            conta_selecionada = next((c for c in contas if c.numero == num), None)
            if conta_selecionada:
                conta_selecionada.ver_extrato()
            else:
                print("Conta não encontrada.")
        elif opcao == "8":
            print("Encerrando o sistema bancário...")
            break
    else:
        print("Conta não encontrada.")

if __name__ == "__main__":
    main()