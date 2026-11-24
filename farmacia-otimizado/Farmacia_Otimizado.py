# Declaração de autoria
# Autores: Levi Matheus, Vinicius Batista, Ezequiel Azevedo
# Declaro que este código foi desenvolvido por mim, com base no meu próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.

from datetime import datetime, date

nroRegistro = 0
raiz = None
movimentacoes = []
pilhaDesfazer = []


class No:
    def __init__(self, medicamento):
        self.medicamento = medicamento
        self.esquerda = None
        self.direita = None
        self.altura = 1


def altura(no):
    if no is None:
        return 0
    return no.altura


def atualizarAltura(no):
    no.altura = 1 + max(altura(no.esquerda), altura(no.direita))


def fatorBalanceamento(no):
    if no is None:
        return 0
    return altura(no.esquerda) - altura(no.direita)


def rotacaoDireita(y):
    x = y.esquerda
    varApoio = x.direita

    x.direita = y
    y.esquerda = varApoio

    atualizarAltura(y)
    atualizarAltura(x)
    return x


def rotacaoEsquerda(x):
    y = x.direita
    varApoio = y.esquerda

    y.esquerda = x
    x.direita = varApoio

    atualizarAltura(x)
    atualizarAltura(y)
    return y


def balancear(no):
    if no is None:
        return None

    atualizarAltura(no)
    fator = fatorBalanceamento(no)

    if fator > 1:
        if fatorBalanceamento(no.esquerda) < 0:
            no.esquerda = rotacaoEsquerda(no.esquerda)
        return rotacaoDireita(no)

    if fator < -1:
        if fatorBalanceamento(no.direita) > 0:
            no.direita = rotacaoDireita(no.direita)
        return rotacaoEsquerda(no)

    return no


def inserir(no, medicamento):
    if no is None:
        return No(medicamento)

    if medicamento["registro"] < no.medicamento["registro"]:
        no.esquerda = inserir(no.esquerda, medicamento)
    elif medicamento["registro"] > no.medicamento["registro"]:
        no.direita = inserir(no.direita, medicamento)
    else:
        return no

    return balancear(no)


def menorNo(no):
    atual = no
    while atual.esquerda is not None:
        atual = atual.esquerda
    return atual


def remover(no, registro):
    if no is None:
        return None

    if registro < no.medicamento["registro"]:
        no.esquerda = remover(no.esquerda, registro)
    elif registro > no.medicamento["registro"]:
        no.direita = remover(no.direita, registro)
    else:
        if no.esquerda is None:
            return no.direita
        elif no.direita is None:
            return no.esquerda
        else:
            sucessor = menorNo(no.direita)
            no.medicamento = sucessor.medicamento
            no.direita = remover(no.direita, sucessor.medicamento["registro"])

    return balancear(no)


def buscarRegistro(no, registro):
    if no is None:
        return None
    if registro == no.medicamento["registro"]:
        return no.medicamento
    if registro < no.medicamento["registro"]:
        return buscarRegistro(no.esquerda, registro)
    return buscarRegistro(no.direita, registro)


def buscarNome(no, nome):
    if no is None:
        return None

    if no.medicamento["nome"].lower() == nome.lower():
        return no.medicamento

    encontrado = buscarNome(no.esquerda, nome)
    if encontrado is not None:
        return encontrado
    return buscarNome(no.direita, nome)


def emOrdem(no, lista):
    if no is not None:
        emOrdem(no.esquerda, lista)
        lista.append(no.medicamento)
        emOrdem(no.direita, lista)


def preOrdem(no, lista):
    if no is not None:
        lista.append(no.medicamento)
        preOrdem(no.esquerda, lista)
        preOrdem(no.direita, lista)


def posOrdem(no, lista):
    if no is not None:
        posOrdem(no.esquerda, lista)
        posOrdem(no.direita, lista)
        lista.append(no.medicamento)


def mergeSort(lista):
    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2
    esquerda = mergeSort(lista[:meio])
    direita = mergeSort(lista[meio:])

    return juntarListas(esquerda, direita)


def juntarListas(esquerda, direita):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if esquerda[i]["nome"].lower() <= direita[j]["nome"].lower():
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado


def chavePrioridade(med):
    return (med["criticidade"], med["validade"], med["nome"].lower())


def inserirHeap(fila, med):
    fila.append(med)
    i = len(fila) - 1

    while i > 0:
        pai = (i - 1) // 2
        if chavePrioridade(fila[i]) < chavePrioridade(fila[pai]):
            fila[i], fila[pai] = fila[pai], fila[i]
            i = pai
        else:
            break


def removerHeap(fila):
    if fila == []:
        return None

    primeiro = fila[0]
    ultimo = fila.pop()

    if fila != []:
        fila[0] = ultimo
        i = 0

        while True:
            esq = 2 * i + 1
            dir = 2 * i + 2
            menor = i

            if esq < len(fila) and chavePrioridade(fila[esq]) < chavePrioridade(fila[menor]):
                menor = esq
            if dir < len(fila) and chavePrioridade(fila[dir]) < chavePrioridade(fila[menor]):
                menor = dir

            if menor != i:
                fila[i], fila[menor] = fila[menor], fila[i]
                i = menor
            else:
                break

    return primeiro


print("FARMÁCIAS BAHIA")

while True:
    listaAuxiliar = []
    emOrdem(raiz, listaAuxiliar)

    filaPrioridade = []
    for med in listaAuxiliar:
        if (med["validade"] - date.today()).days <= 30:
            inserirHeap(filaPrioridade, med)

    if filaPrioridade != []:
        print("\n --- ATENÇÃO!! --- ")
        print(f"Existem {len(filaPrioridade)} medicamentos próximos da data de validade, seguem: ")
        i = 1
        while filaPrioridade != []:
            medVencendo = removerHeap(filaPrioridade)
            print(f"{i} -- {medVencendo['nome']}, Vence em: {medVencendo['validade'].strftime('%d/%m/%Y')}, Nível de criticidade: {medVencendo['criticidade']}")
            i += 1

    print("\n==== Bem-vindo (a) ao sistema! =====")
    print("1. Listar medicamentos")
    print("2. Cadastrar medicamentos")
    print("3. Buscar no estoque")
    print("4. Movimentações de lote")
    print("5. Remover do estoque")
    print("6. Atualizar medicamento")
    print("7. Exibir travessias da árvore")
    print("8. Relatório ordenado por nome")
    print("9. Desfazer última movimentação")
    print("0. Sair do sistema")

    try:
        opcao = int(input("Selecione a opção desejada. "))
    except ValueError:
        print("Opção inválida! Digite uma opção do menu. ")
        continue

    if opcao == 0:
        print("Encerrando sistema...")
        break

    elif opcao == 1:
        print("\n-------- OPÇÃO SELECIONADA: 1. Listar medicamentos -------")
        listaMed = []
        emOrdem(raiz, listaMed)

        if listaMed == []:
            print("Não existem medicamentos cadastrados até então!")
        else:
            print('-=' * 6 + " LISTA DE MEDICAMENTOS " + '=-' * 6)
            for i in range(len(listaMed)):
                print(f"Número de registro: {listaMed[i]['registro']}")
                print('=' * 20)
                print(f"Nome do medicamento: {listaMed[i]['nome']}")
                print('=' * 20)
                print(f"Quantidade disponível: {listaMed[i]['qtd']}")
                print('=' * 20)
                print(f"Preço do medicamento: R${listaMed[i]['preco']:.2f}")
                print('=' * 20)
                print(f"Data de validade: {listaMed[i]['validade'].strftime('%d/%m/%Y')}")
                print('=' * 20)
                print(f"Nível de criticidade/procura do produto: {listaMed[i]['criticidade']}")
                print('=' * 20)
                print(f"Fornecedor: {listaMed[i]['fornecedor']}")
                print(f"CNPJ do fornecedor: {listaMed[i]['cnpjFor']}")
                print('=' * 20)

    elif opcao == 2:
        repetir = 's'
        while repetir == 's':
            print("\n-------- OPÇÃO SELECIONADA: 2. Cadastrar medicamentos -------")
            print("Favor preencher as informações necessárias.")
            print('=' * 40)
            print(f"Nº de registro: {nroRegistro + 1}")
            nroRegistro += 1
            print('-' * 40)

            while True:
                nomeMed = input("Nome do medicamento: ").strip()
                if nomeMed == "":
                    print("O nome não pode ficar vazio! ")
                else:
                    break
            print('-' * 40)

            while True:
                try:
                    quantidadeMed = int(input("Quantidade do medicamento: "))
                    if quantidadeMed <= 0:
                        print("Quantidade inválida! ")
                    else:
                        break
                except ValueError:
                    print("Quantidade inválida! ")
            print('-' * 40)

            while True:
                try:
                    preco = float(input("Informe o valor do medicamento em R$ ").replace(',', '.'))
                    if preco < 0:
                        print("Valor inválido! ")
                    else:
                        break
                except ValueError:
                    print("Valor inválido! ")
            print('-' * 40)

            print("ESCALA DE CRITICIDADE DE MEDICAMENTO: 1 - Essencial | 2 - Comum | 3 - Baixa")
            while True:
                try:
                    criticidade = int(input("Indique o nível de criticidade do medicamento baseado na procura: "))
                    if criticidade != 1 and criticidade != 2 and criticidade != 3:
                        print("O nível de criticidade é de 1-3. ")
                    else:
                        break
                except ValueError:
                    print("O nível de criticidade é de 1-3. ")
            print('-' * 40)

            while True:
                try:
                    validade = datetime.strptime(input("Informe a data de validade do medicamento no formato dd/mm/aaaa. "), "%d/%m/%Y").date()
                    if validade <= date.today():
                        print("O medicamento já está vencido! Insira uma data de validade válida.")
                    else:
                        break
                except ValueError:
                    print("Formato inválido! Digite uma data válida no formato 'dd/mm/aaaa'.")

            print("-=-=-=-=-= INFORMAÇÕES DO FORNECEDOR -=-=-=-=-=")

            while True:
                fornecedor = input("Informe o nome do fornecedor do medicamento: ").strip()
                if fornecedor == "":
                    print("O fornecedor não pode ser nenhum! ")
                else:
                    break
            print('-' * 40)

            while True:
                cnpj = input("Informe o CNPJ do fornecedor: ").strip()
                if cnpj.isnumeric() and len(cnpj) == 14:
                    cnpj = cnpj[:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:]
                    break
                else:
                    print("CNPJ inválido! Insira apenas os 14 números do CNPJ do fornecedor.")

            novoMed = {
                "nome": nomeMed,
                "registro": nroRegistro,
                "qtd": quantidadeMed,
                "preco": preco,
                "validade": validade,
                "criticidade": criticidade,
                "fornecedor": fornecedor,
                "cnpjFor": cnpj
            }

            raiz = inserir(raiz, novoMed)
            pilhaDesfazer.append({"acao": "adicionar", "medicamento": novoMed.copy()})
            movimentacoes.insert(0, f"Medicamento {nomeMed} ADICIONADO ao estoque")

            print('-' * 40)
            print("Pronto! Medicamento cadastrado com sucesso!")
            while True:
                repetir = input("Deseja adicionar mais algum medicamento? (S/N) ").lower()
                if repetir != 's' and repetir != 'n':
                    print("Favor, informar se deseja adicionar mais algum medicamento. ")
                else:
                    break

    elif opcao == 3:
        print("\n-------- OPÇÃO SELECIONADA: 3. Busca no estoque -------")
        if raiz is None:
            print("Não existem medicamentos cadastrados no sistema ainda. ")
        else:
            busca = input("Digite o nome ou número de registro do medicamento que deseja buscar: ").strip()

            if busca.isnumeric():
                encontrado = buscarRegistro(raiz, int(busca))
            else:
                encontrado = buscarNome(raiz, busca)

            if encontrado is None:
                print("O medicamento não foi encontrado. ")
            else:
                print("Medicamento encontrado no sistema: ")
                print(f"Nrº: {encontrado['registro']}, Nome: {encontrado['nome']}, Qtd: {encontrado['qtd']}, Validade: {encontrado['validade'].strftime('%d/%m/%Y')}, Valor: R$ {encontrado['preco']:.2f}")

    elif opcao == 4:
        print("\n-------- OPÇÃO SELECIONADA: 4. Movimentações de lote -------")
        if movimentacoes == []:
            print("Não existem movimentações registradas no sistema.")
        else:
            print("-=" * 6 + " MOVIMENTAÇÕES DE LOTE " + "=-" * 6)
            for i in range(len(movimentacoes)):
                print(f"\n----- {i + 1}. {movimentacoes[i]};")

    elif opcao == 5:
        print("\n-------- OPÇÃO SELECIONADA: 5. Remover do estoque -------")
        listaMed = []
        emOrdem(raiz, listaMed)

        if listaMed == []:
            print("Não existem medicamentos cadastrados no sistema. ")
        else:
            print('-=' * 6 + " LISTA DE MEDICAMENTOS " + '=-' * 6)
            for i in range(len(listaMed)):
                print(f"Número de registro: {listaMed[i]['registro']}")
                print('=' * 20)
                print(f"Nome do medicamento: {listaMed[i]['nome']}")
                print('=' * 20)
                print(f"Quantidade disponível: {listaMed[i]['qtd']}")
                print('=' * 20)
                print(f"Preço do medicamento: R${listaMed[i]['preco']:.2f}")
                print('=' * 20)
                print(f"Nível de criticidade/procura do produto: {listaMed[i]['criticidade']}")
                print('=' * 20)
                print(f"Fornecedor: {listaMed[i]['fornecedor']}")
                print(f"CNPJ do fornecedor: {listaMed[i]['cnpjFor']}")
                print('=' * 20)

            try:
                removerEstoque = int(input("Digite o Nº de registro do medicamento que deseja remover: "))
                medEncontrado = buscarRegistro(raiz, removerEstoque)

                if medEncontrado is None:
                    print("Nº de registro não identificado. ")
                else:
                    copia = medEncontrado.copy()
                    raiz = remover(raiz, removerEstoque)
                    pilhaDesfazer.append({"acao": "remover", "medicamento": copia})
                    movimentacoes.insert(0, f"Medicamento {copia['nome']} REMOVIDO do estoque")
                    print(f"Medicamento {copia['nome']} removido com sucesso!")
            except ValueError:
                print("Nº de registro não identificado. ")

    elif opcao == 6:
        print("\n-------- OPÇÃO SELECIONADA: 6. Atualizar medicamento -------")
        if raiz is None:
            print("Não existem medicamentos cadastrados no sistema. ")
        else:
            try:
                registroAtualizar = int(input("Digite o Nº de registro do medicamento que deseja atualizar: "))
            except ValueError:
                print("Nº de registro não identificado. ")
                continue

            medicamento = buscarRegistro(raiz, registroAtualizar)

            if medicamento is None:
                print("Nº de registro não identificado. ")
            else:
                anterior = medicamento.copy()
                print("Pressione ENTER caso queira manter o valor atual.")
                print('-' * 40)

                novoNome = input(f"Nome [{medicamento['nome']}]: ").strip()
                if novoNome != "":
                    medicamento["nome"] = novoNome

                novaQtd = input(f"Quantidade [{medicamento['qtd']}]: ").strip()
                if novaQtd != "":
                    while True:
                        try:
                            valorQtd = int(novaQtd)
                            if valorQtd <= 0:
                                print("Quantidade inválida! ")
                            else:
                                medicamento["qtd"] = valorQtd
                                break
                        except ValueError:
                            print("Quantidade inválida! ")
                        novaQtd = input("Quantidade do medicamento: ").strip()

                novoPreco = input(f"Preço R$ [{medicamento['preco']:.2f}]: ").strip()
                if novoPreco != "":
                    while True:
                        try:
                            valorPreco = float(novoPreco.replace(',', '.'))
                            if valorPreco < 0:
                                print("Valor inválido! ")
                            else:
                                medicamento["preco"] = valorPreco
                                break
                        except ValueError:
                            print("Valor inválido! ")
                        novoPreco = input("Informe o valor do medicamento em R$ ").strip()

                novaCrit = input(f"Criticidade [{medicamento['criticidade']}]: ").strip()
                if novaCrit != "":
                    while True:
                        try:
                            valorCrit = int(novaCrit)
                            if valorCrit != 1 and valorCrit != 2 and valorCrit != 3:
                                print("O nível de criticidade é de 1-3. ")
                            else:
                                medicamento["criticidade"] = valorCrit
                                break
                        except ValueError:
                            print("O nível de criticidade é de 1-3. ")
                        novaCrit = input("Indique o nível de criticidade (1-3): ").strip()

                novaValidade = input(f"Validade [{medicamento['validade'].strftime('%d/%m/%Y')}]: ").strip()
                if novaValidade != "":
                    while True:
                        try:
                            dataConvertida = datetime.strptime(novaValidade, "%d/%m/%Y").date()
                            if dataConvertida <= date.today():
                                print("O medicamento já está vencido! Insira uma data de validade válida.")
                            else:
                                medicamento["validade"] = dataConvertida
                                break
                        except ValueError:
                            print("Formato inválido! Digite uma data válida no formato 'dd/mm/aaaa'.")
                        novaValidade = input("Informe a data de validade (dd/mm/aaaa): ").strip()

                novoFornecedor = input(f"Fornecedor [{medicamento['fornecedor']}]: ").strip()
                if novoFornecedor != "":
                    medicamento["fornecedor"] = novoFornecedor

                novoCnpj = input(f"CNPJ [{medicamento['cnpjFor']}]: ").strip()
                if novoCnpj != "":
                    while True:
                        if novoCnpj.isnumeric() and len(novoCnpj) == 14:
                            medicamento["cnpjFor"] = novoCnpj[:2] + '.' + novoCnpj[2:5] + '.' + novoCnpj[5:8] + '/' + novoCnpj[8:12] + '-' + novoCnpj[12:]
                            break
                        else:
                            print("CNPJ inválido! Insira apenas os 14 números do CNPJ do fornecedor.")
                            novoCnpj = input("Informe o CNPJ do fornecedor: ").strip()

                pilhaDesfazer.append({"acao": "atualizar", "anterior": anterior, "atual": medicamento.copy()})
                movimentacoes.insert(0, f"Medicamento {medicamento['nome']} ATUALIZADO no estoque")
                print('-' * 40)
                print("Medicamento atualizado com sucesso!")

    elif opcao == 7:
        print("\n-------- OPÇÃO SELECIONADA: 7. Exibir travessias da árvore -------")
        if raiz is None:
            print("Não existem medicamentos cadastrados até então!")
        else:
            listaIn = []
            emOrdem(raiz, listaIn)
            print('-=' * 6 + " EM ORDEM " + '=-' * 6)
            for i in range(len(listaIn)):
                print(f"Nrº: {listaIn[i]['registro']} - {listaIn[i]['nome']} (Qtd: {listaIn[i]['qtd']})")

            listaPre = []
            preOrdem(raiz, listaPre)
            print('\n' + '-=' * 6 + " PRÉ-ORDEM " + '=-' * 6)
            for i in range(len(listaPre)):
                print(f"Nrº: {listaPre[i]['registro']} - {listaPre[i]['nome']} (Qtd: {listaPre[i]['qtd']})")

            listaPos = []
            posOrdem(raiz, listaPos)
            print('\n' + '-=' * 6 + " PÓS-ORDEM " + '=-' * 6)
            for i in range(len(listaPos)):
                print(f"Nrº: {listaPos[i]['registro']} - {listaPos[i]['nome']} (Qtd: {listaPos[i]['qtd']})")

    elif opcao == 8:
        print("\n-------- OPÇÃO SELECIONADA: 8. Relatório ordenado por nome -------")
        listaMed = []
        emOrdem(raiz, listaMed)

        if listaMed == []:
            print("Não existem medicamentos cadastrados até então!")
        else:
            listaOrdenada = mergeSort(listaMed)
            print('-=' * 6 + " LISTA ORDENADA POR NOME " + '=-' * 6)
            for i in range(len(listaOrdenada)):
                print(f"Número de registro: {listaOrdenada[i]['registro']}")
                print('=' * 20)
                print(f"Nome do medicamento: {listaOrdenada[i]['nome']}")
                print('=' * 20)
                print(f"Quantidade disponível: {listaOrdenada[i]['qtd']}")
                print('=' * 20)
                print(f"Preço do medicamento: R${listaOrdenada[i]['preco']:.2f}")
                print('=' * 20)
                print(f"Data de validade: {listaOrdenada[i]['validade'].strftime('%d/%m/%Y')}")
                print('=' * 20)
                print(f"Nível de criticidade/procura do produto: {listaOrdenada[i]['criticidade']}")
                print('=' * 20)
                print(f"Fornecedor: {listaOrdenada[i]['fornecedor']}")
                print(f"CNPJ do fornecedor: {listaOrdenada[i]['cnpjFor']}")
                print('=' * 20)

    elif opcao == 9:
        print("\n-------- OPÇÃO SELECIONADA: 9. Desfazer última movimentação -------")
        if pilhaDesfazer == []:
            print("Não existem movimentações para desfazer.")
        else:
            ultimaAcao = pilhaDesfazer.pop()

            if ultimaAcao["acao"] == "adicionar":
                med = ultimaAcao["medicamento"]
                raiz = remover(raiz, med["registro"])
                msg = f"Cadastro do medicamento {med['nome']} DESFEITO"

            elif ultimaAcao["acao"] == "remover":
                med = ultimaAcao["medicamento"]
                raiz = inserir(raiz, med)
                msg = f"Remoção do medicamento {med['nome']} DESFEITA"

            else:
                atual = ultimaAcao["atual"]
                anterior = ultimaAcao["anterior"]
                raiz = remover(raiz, atual["registro"])
                raiz = inserir(raiz, anterior)
                msg = f"Atualização do medicamento {anterior['nome']} DESFEITA"

            movimentacoes.insert(0, msg)
            print(msg)

    else:
        print("Opção inválida! Digite uma opção do menu. ")