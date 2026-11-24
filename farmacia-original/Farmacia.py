# Declaração de autoria
# Autores: Levi Matheus, Vinicius Batista, Ezequiel Azevedo
# Declaro que este código foi desenvolvido por mim, com base no meu próprio
# entendimento e esforço. Não houve plágio ou cópia integral de terceiros.
# Ferramentas de IA, quando utilizadas, foram apenas como apoio ao aprendizado
# e não para a geração integral deste código.


from datetime import datetime, date
from queue import PriorityQueue

nroRegistro = 0
listaMed = []
movimentacoes = []

def ordenadoPorNome (lista):
     for i in range (1, len(lista)):
          chave = lista[i]
          varApoio = i - 1

          while varApoio >= 0 and lista[varApoio]["nome"].lower() > chave["nome"].lower():
               lista[varApoio + 1] = lista[varApoio]
               varApoio = varApoio - 1
          lista[varApoio + 1] = chave



print("FARMÁCIAS BAHIA")

while True:
    filaPrioridade = PriorityQueue()
    for med in listaMed:
        if (med["validade"] - date.today()).days <= 30:
            filaPrioridade.put((med["criticidade"], med["validade"], med["nome"]))

    if not filaPrioridade.empty():
     print(" --- ATENÇÃO!! --- ")
     print(f"Existem {filaPrioridade.qsize()} medicamentos próximos da data de validade, seguem: ")
     i = 1
     while not filaPrioridade.empty():
          urgencia, data, medicamento = filaPrioridade.get()
          print(f"{i} -- {medicamento}, Vence em: {data}, Nível de criticidade: {urgencia}")
          i += 1


    print("\n==== Bem-vindo (a) ao sistema! =====")
    print("1. Listar medicamentos")
    print("2. Cadastrar medicamentos")
    print("3. Buscar no estoque")
    print("4. Movimentações de lote")
    print("5. Remover do estoque")
    print("0. Sair do sistema")

    opcao = int(input("Selecione a opção desejada. "))

    if opcao == 0:
        print("Encerrando sistema...")
        break
    
    elif opcao == 2:
        repetir = 's'
        while repetir == 's':
          print("\n-------- OPÇÃO SELECIONADA: 2. Cadastrar medicamentos -------")
          print("Favor preencher as informações necessárias.")
          print('='*40)
          print(f"Nº de registro: {nroRegistro + 1}")
          nroRegistro +=1
          print('-'*40)
          while True:
               nomeMed = input("Nome do medicamento: ")
               if nomeMed == "":
                    print("O nome não pode ficar vazio! ")
               else:
                    break
          print('-'*40)
          while True:
               quantidadeMed = int(input("Quantidade do medicamento: "))
               if quantidadeMed <= 0:
                    print("Quantidade inválida! ")
               else:
                    break
          print('-'*40)
          while True:
               preco = float(input ("Informe o valor do medicamento em R$ ").replace(',','.'))
               if preco < 0:
                    print("Valor inválido! ")
               else:
                    break
          print('-'*40)
          print("ESCALA DE CRITICIDADE DE MEDICAMENTO: 1 - Essencial | 2 - Comum | 3 - Baixa")
          while True:
               criticidade = int(input("Indique o nível de criticidade do medicamento baseado na procura: "))
               if criticidade != 1 and criticidade != 2 and criticidade != 3:
                    print("O nível de criticidade é de 1-3. ")
               else:
                    break 
          print('-'*40)
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
               fornecedor = input("Informe o nome do fornecedor do medicamento: ")
               if fornecedor == "":
                    print("O fornecedor não pode ser nenhum! ")
               else:
                    break
          print('-'*40)
          while True:
               cnpj = input("Informe o CNPJ do fornecedor: ")

               if cnpj.isnumeric() and len(cnpj) == 14:
                    cnpj = cnpj[:2] + '.' + cnpj[2:5] + '.' + cnpj[5:8] + '/' + cnpj[8:12] + '-' + cnpj[12:] 
                    break
               else:
                    print("CNPJ inválido! Insira apenas os 14 números do CNPJ do fornecedor.")

          listaMed.append({
                       "nome": nomeMed,
                       "registro": nroRegistro,
                       "qtd": quantidadeMed,
                       "preco": preco,
                       "validade": validade,
                       "criticidade": criticidade, 
                       "fornecedor": fornecedor,
                       "cnpjFor": cnpj
                  }) 
          movimentacoes.insert(0, f"Medicamento {listaMed[len(listaMed)-1]["nome"]} ADICIONADO ao estoque") 
         
          print('-'*40)
          print("Pronto! Medicamento cadastrado com sucesso!")
          while True:
               repetir = input("Deseja adicionar mais algum medicamento? (S/N) ").lower()
               if repetir != 's' and repetir != 'n':
                    print("Favor, informar se deseja adicionar mais algum medicamento. ")
               else:
                    break

    elif opcao == 1:
         print("\n-------- OPÇÃO SELECIONADA: 1. Listar medicamentos -------")

         if listaMed == []:
              print("Não existem medicamentos cadastrados até então!") 
         else:
              print('-='*6 + " LISTA DE MEDICAMENTOS " + '=-'*6)
              for i in range(len(listaMed)):
                   print(f"Número de registro: {listaMed[i]["registro"]}")
                   print('='*20)
                   print(f"Nome do medicamento: {listaMed[i]["nome"]}")
                   print('='*20)
                   print(f"Quantidade disponível: {listaMed[i]["qtd"]}")
                   print('='*20)
                   print(f"Preço do medicamento: R${listaMed[i]["preco"]:.2f}")
                   print('='*20)
                   print(f"Nível de criticidade/procura do produto: {listaMed[i]["criticidade"]}")
                   print('='*20)
                   print(f'Fornecedor: {listaMed[i]["fornecedor"]}')
                   print(f"CNPJ do fornecedor: {listaMed[i]["cnpjFor"]}")

                   print('='*20)

    elif opcao == 4:

         print("\n-------- OPÇÃO SELECIONADA: 4. Movimentações de lote -------")
         if movimentacoes == []:
          print("Não existem movimentações registradas no sistema.")    
         else: 
          print("-="*6 + " MOVIMENTAÇÕES DE LOTE " + "=-"*6)

          for i in range(len(movimentacoes)):
               print(f"\n----- {i+1}. {movimentacoes[i]};")

          if listaMed == []:
                print("Não há medicamentos no estoque para remover.")
          else:
               while True:
                    remover = input(f"Deseja remover o último medicamento cadastrado ({listaMed[-1]["nome"]})? (S/N) ").lower()
                    if remover != 's' and remover != 'n':
                         print("Opção inválida! Digite S ou N.")
                    else:
                         break

               if remover == 's':
                    itemRemovido = listaMed.pop()
                    movimentacoes.insert(0, f"Medicamento {itemRemovido["nome"]} REMOVIDO do estoque")
                    print(f"Alteração feita! {itemRemovido["nome"]} foi removido do estoque.")
               else:
                    print('='*20)    
    elif opcao == 3:
        print("\n-------- OPÇÃO SELECIONADA: 3. Busca no estoque -------")
        if listaMed == []:
                  print("Não existem medicamentos cadastrados no sistema ainda. ")
        else:
          encontrado = False
          busca = input("Digite o nome ou número de registro do medicamento que deseja buscar: ").strip()

          inicio, fim = 0, len(listaMed) - 1  
          if busca.isnumeric():
               busca = int(busca)
               while inicio <= fim:
                    
                    meio = (inicio + fim) // 2

                    if listaMed[meio]["registro"] == busca:
                         print("Medicamento encontrado no sistema: ")
                         print(f"Nrº: {listaMed[meio]["registro"]}, Nome: {listaMed[meio]["nome"]}, Validade: {listaMed[meio]["validade"]}, Valor: R$ {listaMed[meio]["preco"]}")
                         encontrado = True
                         break
                    elif listaMed[meio]["registro"] < busca:
                         inicio = meio + 1

                    else:
                         fim = meio - 1
               if not encontrado: 
                    print("O medicamento não foi encontrado. ")
                    
          else:
               listaPorNome = listaMed.copy()
               ordenadoPorNome(listaPorNome)
               while inicio <= fim:
                    meio = (inicio + fim) // 2

                    if listaPorNome[meio]["nome"].lower() == busca.lower():
                         print("Medicamento encontrado no sistema: ")
                         print(f"Nrº: {listaPorNome[meio]["registro"]}, Nome: {listaPorNome[meio]["nome"]}, Validade: {listaPorNome[meio]["validade"]}, Valor: R$ {listaPorNome[meio]["preco"]}")
                         encontrado = True
                         break
                    elif listaPorNome[meio]["nome"].lower() < busca.lower():
                         inicio = meio + 1
                    else: 
                         fim = meio - 1
                         
               if not encontrado: 
                    print("O medicamento não foi encontrado. ")  


    elif opcao == 5:
         print("\n-------- OPÇÃO SELECIONADA: 5. Remover do estoque -------")
         if not listaMed:
              print("Não existem medicamentos cadastrados no sistema. ")
         else: 
              print('-='*6 + " LISTA DE MEDICAMENTOS " + '=-'*6)
              for i in range(len(listaMed)):
                    print(f"Número de registro: {listaMed[i]["registro"]}")
                    print('='*20)
                    print(f"Nome do medicamento: {listaMed[i]["nome"]}")
                    print('='*20)
                    print(f"Quantidade disponível: {listaMed[i]["qtd"]}")
                    print('='*20)
                    print(f"Preço do medicamento: R${listaMed[i]["preco"]:.2f}")
                    print('='*20)
                    print(f"Nível de criticidade/procura do produto: {listaMed[i]["criticidade"]}")
                    print('='*20)
                    print(f'Fornecedor: {listaMed[i]["fornecedor"]}')
                    print(f"CNPJ do fornecedor: {listaMed[i]["cnpjFor"]}")
              
                    print('='*20)

              removerEstoque = int(input("Digite o Nº de registro do medicamento que deseja remover: "))

              indice = -1
              for i in range(len(listaMed)):
                    if listaMed[i]["registro"] == removerEstoque:
                         indice = i
                         break

              if indice == -1:
                 print("Nº de registro não identificado. ")
              else:
                 removido = listaMed.pop(indice)
                 movimentacoes.insert(0, f"Medicamento {removido["nome"]} REMOVIDO do estoque")
                 print(f"Medicamento {removido["nome"]} removido com sucesso!")
    else:
         print("Opção inválida! Digite uma opção do menu. ")             