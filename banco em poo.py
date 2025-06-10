from datetime import datetime


class BancoException(Exception):
    pass


class SaldoInsuficiente(BancoException):
    pass


class ContaInexistente(BancoException):
    pass


class Conta:
    def __init__(self, numero, titular, senha, saldo_inicial=0):
        self.numero = numero
        self.titular = titular
        self._senha = senha
        self.saldo = saldo_inicial
        self.historico = []

    def autenticar(self, senha):
        return senha == self._senha

    def alterar_titular(self, novo_nome):
        if novo_nome.strip():
            self.titular = novo_nome.strip()
            print("Nome do titular atualizado com sucesso.")
        else:
            print("Nome inválido.")

    def alterar_senha(self, senha_atual, nova_senha):
        if senha_atual != self._senha:
            print("Senha atual incorreta.")
            return
        if len(nova_senha) < 4:
            print("Nova senha deve ter pelo menos 4 caracteres.")
            return
        self._senha = nova_senha
        print("Senha atualizada com sucesso.")

    def depositar(self, valor):
        if valor <= 0:
            raise BancoException("Valor de depósito inválido.")
        self.saldo += valor
        self.registrar_historico('Depósito', valor)
        print(f"Depósito de R${valor:.2f} realizado com sucesso.")

    def sacar(self, valor):
        if valor <= 0:
            raise BancoException("Valor de saque inválido.")
        if valor > self.saldo:
            raise SaldoInsuficiente("Saldo insuficiente.")
        self.saldo -= valor
        self.registrar_historico('Saque', valor)
        print(f"Saque de R${valor:.2f} realizado com sucesso.")

    def transferir(self, valor, conta_destino):
        if valor <= 0:
            raise BancoException("Valor de transferência inválido.")
        if valor > self.saldo:
            raise SaldoInsuficiente("Saldo insuficiente para transferência.")
        self.sacar(valor)
        conta_destino.depositar(valor)
        self.registrar_historico('Transferência enviada', valor, conta_destino.numero)
        conta_destino.registrar_historico('Transferência recebida', valor, self.numero)
        print(f"Transferência de R${valor:.2f} para a conta {conta_destino.numero} realizada com sucesso.")

    def registrar_historico(self, tipo, valor, conta_destino=None):
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if conta_destino:
            descricao = f"{tipo} de R${valor:.2f} para conta {conta_destino}"
        else:
            descricao = f"{tipo} de R${valor:.2f}"
        self.historico.append(f"{data} - {descricao}")

    def mostrar_saldo(self):
        print(f"Conta {self.numero} - Titular: {self.titular} - Saldo: R${self.saldo:.2f}")

    def extrato(self):
        print(f"\nExtrato da Conta {self.numero} - Titular: {self.titular}")
        if not self.historico:
            print("Nenhuma transação realizada.")
        else:
            for registro in self.historico:
                print(registro)
        print(f"Saldo atual: R${self.saldo:.2f}\n")


class ContaCorrente(Conta):
    def __init__(self, numero, titular, senha, saldo_inicial=0, limite_cheque_especial=0):
        super().__init__(numero, titular, senha, saldo_inicial)
        self.limite_cheque_especial = limite_cheque_especial

    def sacar(self, valor):
        if valor <= 0:
            raise BancoException("Valor de saque inválido.")
        limite_disponivel = self.saldo + self.limite_cheque_especial
        if valor > limite_disponivel:
            raise SaldoInsuficiente("Saldo e limite insuficientes.")
        self.saldo -= valor
        self.registrar_historico('Saque', valor)
        print(f"Saque de R${valor:.2f} realizado com sucesso. (Conta Corrente)")

    def mostrar_saldo(self):
        print(f"Conta Corrente {self.numero} - Titular: {self.titular} - Saldo: R${self.saldo:.2f} - Limite cheque especial: R${self.limite_cheque_especial:.2f}")


class ContaPoupanca(Conta):
    def __init__(self, numero, titular, senha, saldo_inicial=0):
        super().__init__(numero, titular, senha, saldo_inicial)
        self.taxa_juros = 0.005  # 0.5% ao mês

    def render_juros(self):
        juros = self.saldo * self.taxa_juros
        self.saldo += juros
        self.registrar_historico('Rendimento de Juros', juros)
        print(f"Juros de R${juros:.2f} creditados na conta poupança.")


class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = {}

    def abrir_conta(self, tipo, numero, titular, senha, saldo_inicial=0, **kwargs):
        if numero in self.contas:
            raise BancoException("Número de conta já existe.")
        if tipo == 'corrente':
            conta = ContaCorrente(numero, titular, senha, saldo_inicial, kwargs.get('limite_cheque_especial', 0))
        elif tipo == 'poupanca':
            conta = ContaPoupanca(numero, titular, senha, saldo_inicial)
        else:
            raise BancoException("Tipo de conta inválido.")
        self.contas[numero] = conta
        print(f"Conta {tipo} número {numero} aberta com sucesso para {titular}.")

    def fechar_conta(self, numero):
        if numero not in self.contas:
            raise ContaInexistente("Conta não encontrada.")
        del self.contas[numero]
        print(f"Conta {numero} fechada com sucesso.")

    def buscar_conta(self, numero):
        if numero not in self.contas:
            raise ContaInexistente("Conta não encontrada.")
        return self.contas[numero]

    def listar_contas(self):
        print(f"\nContas do Banco {self.nome}:")
        if not self.contas:
            print("Nenhuma conta cadastrada.")
        else:
            for conta in self.contas.values():
                conta.mostrar_saldo()


def menu():
    banco = Banco("Banco Python")

    # Abrir contas de exemplo
    banco.abrir_conta('corrente', 101, 'Pedro', '1234', 1500, limite_cheque_especial=500)
    banco.abrir_conta('poupanca', 202, 'Ana', '4321', 1000)

    while True:
        print("\n--- Sistema Bancário ---")
        print("1 - Acessar Conta")
        print("2 - Listar Contas")
        print("3 - Abrir Conta")
        print("4 - Fechar Conta")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            try:
                numero = int(input("Número da conta: "))
                conta = banco.buscar_conta(numero)
                senha = input("Senha: ")
                if not conta.autenticar(senha):
                    print("Senha incorreta.")
                    continue
                submenu_conta(conta, banco)
            except BancoException as e:
                print("Erro:", e)
            except ValueError:
                print("Número inválido.")
        elif opcao == '2':
            banco.listar_contas()
        elif opcao == '3':
            try:
                tipo = input("Tipo da conta (corrente/poupanca): ").lower()
                numero = int(input("Número da conta: "))
                titular = input("Nome do titular: ")
                senha = input("Senha (mínimo 4 caracteres): ")
                if len(senha) < 4:
                    print("Senha muito curta.")
                    continue
                saldo = float(input("Saldo inicial: "))
                if tipo == 'corrente':
                    limite = float(input("Limite cheque especial: "))
                    banco.abrir_conta(tipo, numero, titular, senha, saldo, limite_cheque_especial=limite)
                else:
                    banco.abrir_conta(tipo, numero, titular, senha, saldo)
            except BancoException as e:
                print("Erro:", e)
            except ValueError:
                print("Entrada inválida.")
        elif opcao == '4':
            try:
                numero = int(input("Número da conta para fechar: "))
                banco.fechar_conta(numero)
            except BancoException as e:
                print("Erro:", e)
            except ValueError:
                print("Número inválido.")
        elif opcao == '0':
            print("Encerrando o sistema. Obrigado!")
            break
        else:
            print("Opção inválida.")


def submenu_conta(conta, banco):
    while True:
        print(f"\n--- Conta {conta.numero} - {conta.titular} ---")
        print("1 - Mostrar Saldo")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Transferir")
        print("5 - Extrato")
        print("6 - Alterar Nome do Titular")
        print("7 - Alterar Senha")
        if isinstance(conta, ContaPoupanca):
            print("8 - Render Juros")
            print("0 - Sair da Conta")
        else:
            print("0 - Sair da Conta")

        opcao = input("Escolha uma opção: ")

        try:
            if opcao == '1':
                conta.mostrar_saldo()
            elif opcao == '2':
                valor = float(input("Valor para depósito: "))
                conta.depositar(valor)
            elif opcao == '3':
                valor = float(input("Valor para saque: "))
                conta.sacar(valor)
            elif opcao == '4':
                valor = float(input("Valor para transferência: "))
                destino_num = int(input("Número da conta destino: "))
                conta_destino = banco.buscar_conta(destino_num)
                conta.transferir(valor, conta_destino)
            elif opcao == '5':
                conta.extrato()
            elif opcao == '6':
                novo_nome = input("Novo nome do titular: ")
                conta.alterar_titular(novo_nome)
            elif opcao == '7':
                senha_atual = input("Senha atual: ")
                nova_senha = input("Nova senha: ")
                conta.alterar_senha(senha_atual, nova_senha)
            elif opcao == '8' and isinstance(conta, ContaPoupanca):
                conta.render_juros()
            elif opcao == '0':
                print("Saindo da conta...")
                break
            else:
                print("Opção inválida.")
        except BancoException as e:
            print("Erro:", e)
        except ValueError:
            print("Entrada inválida.")


if __name__ == "__main__":
    menu()
