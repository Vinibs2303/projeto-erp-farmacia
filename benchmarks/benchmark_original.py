# BENCHMARK - CODIGO ORIGINAL
# Este arquivo reproduz as funcoes de estrutura de dados do sistema enviado
# para medir o desempenho sem executar o menu interativo.

import time
import random
from datetime import date, timedelta


def ordenadoPorNome(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        varApoio = i - 1

        while varApoio >= 0 and lista[varApoio]["nome"].lower() > chave["nome"].lower():
            lista[varApoio + 1] = lista[varApoio]
            varApoio -= 1

        lista[varApoio + 1] = chave


def buscarRegistro(lista, registro):
    inicio = 0
    fim = len(lista) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if lista[meio]["registro"] == registro:
            return lista[meio]

        elif lista[meio]["registro"] < registro:
            inicio = meio + 1

        else:
            fim = meio - 1

    return None


def buscarNome(lista, nome):
    listaPorNome = lista.copy()
    ordenadoPorNome(listaPorNome)

    inicio = 0
    fim = len(listaPorNome) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2

        if listaPorNome[meio]["nome"].lower() == nome.lower():
            return listaPorNome[meio]

        elif listaPorNome[meio]["nome"].lower() < nome.lower():
            inicio = meio + 1

        else:
            fim = meio - 1

    return None


def removerRegistro(lista, registro):
    indice = -1

    for i in range(len(lista)):
        if lista[i]["registro"] == registro:
            indice = i
            break

    if indice != -1:
        lista.pop(indice)


def criarDados(quantidade, cenario):
    lista = []

    for i in range(quantidade):
        lista.append({
            "nome": f"Medicamento {i:05d}",
            "registro": i + 1,
            "qtd": 100,
            "preco": 10.0,
            "validade": date.today() + timedelta(days=100),
            "criticidade": 2,
            "fornecedor": "Fornecedor Teste",
            "cnpjFor": "00.000.000/0000-00"
        })

    if cenario == "aleatorio":
        random.shuffle(lista)

    elif cenario == "inverso":
        lista.reverse()

    return lista


volumes = [100, 1000, 10000]
cenarios = ["aleatorio", "ordenado", "inverso"]
repeticoes = 5

print("BENCHMARK - VERSÃO ORIGINAL")

for volume in volumes:
    for cenario in cenarios:

        tempos_ordenacao = []
        tempos_busca_nome = []
        tempos_busca_registro = []
        tempos_remocao = []
        tempos_listagem = []

        for repeticao in range(repeticoes):

            dados = criarDados(volume, cenario)

            lista = dados.copy()

            inicio = time.perf_counter()
            ordenadoPorNome(lista)
            fim = time.perf_counter()

            tempos_ordenacao.append((fim - inicio) * 1000)

            inicio = time.perf_counter()
            buscarNome(dados, f"Medicamento {volume - 1:05d}")
            fim = time.perf_counter()

            tempos_busca_nome.append((fim - inicio) * 1000)

            dados_registro = sorted(dados, key=lambda item: item["registro"])

            inicio = time.perf_counter()
            buscarRegistro(dados_registro, volume)
            fim = time.perf_counter()

            tempos_busca_registro.append((fim - inicio) * 1000)

            lista_remocao = dados.copy()

            inicio = time.perf_counter()
            removerRegistro(lista_remocao, volume)
            fim = time.perf_counter()

            tempos_remocao.append((fim - inicio) * 1000)

            inicio = time.perf_counter()
            for medicamento in dados:
                medicamento["nome"]
            fim = time.perf_counter()

            tempos_listagem.append((fim - inicio) * 1000)

        media_ordenacao = sum(tempos_ordenacao) / repeticoes
        media_busca_nome = sum(tempos_busca_nome) / repeticoes
        media_busca_registro = sum(tempos_busca_registro) / repeticoes
        media_remocao = sum(tempos_remocao) / repeticoes
        media_listagem = sum(tempos_listagem) / repeticoes

        print(f"\nVolume: {volume} registros | Cenário: {cenario}")
        print(f"Ordenação: {media_ordenacao:.6f} ms")
        print(f"Busca por nome: {media_busca_nome:.6f} ms")
        print(f"Busca por registro: {media_busca_registro:.6f} ms")
        print(f"Remoção: {media_remocao:.6f} ms")
        print(f"Listagem: {media_listagem:.6f} ms")
