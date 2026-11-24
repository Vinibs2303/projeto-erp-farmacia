# BENCHMARK - CODIGO OTIMIZADO
# Este arquivo reproduz as funcoes de estrutura de dados do sistema enviado
# para medir o desempenho sem executar o menu interativo.

from datetime import date, timedelta
from time import perf_counter
import random
import csv

VOLUMES = [100, 1000, 10000]
CENARIOS = ["aleatorio", "ordenado", "inverso"]
REPETICOES = 5

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


def criarDados(quantidade, cenario):
    dados = []

    for i in range(1, quantidade + 1):
        dados.append({
            "nome": f"Medicamento {i:05d}",
            "registro": i,
            "qtd": 100,
            "preco": 10.0,
            "validade": date.today() + timedelta(days=(i % 365) + 1),
            "criticidade": (i % 3) + 1,
            "fornecedor": "Fornecedor Teste",
            "cnpjFor": "00.000.000/0000-00"
        })

    if cenario == "aleatorio":
        random.Random(42).shuffle(dados)
    elif cenario == "inverso":
        dados.reverse()

    return dados


def medir(funcao):
    inicio = perf_counter()
    funcao()
    fim = perf_counter()
    return (fim - inicio) * 1000


def construirArvore(dados):
    raiz = None
    for med in dados:
        raiz = inserir(raiz, med)
    return raiz


def benchmark():
    resultados = []

    print("\n========== BENCHMARK - CODIGO OTIMIZADO ==========")
    print(f"Repeticoes por teste: {REPETICOES}")

    for volume in VOLUMES:
        for cenario in CENARIOS:
            tempos = {
                "Insercao AVL": [],
                "Busca por registro existente": [],
                "Busca por registro inexistente": [],
                "Busca por nome existente": [],
                "Busca por nome inexistente": [],
                "Remocao AVL": [],
                "Travessia em ordem": [],
                "Travessia pre-ordem": [],
                "Travessia pos-ordem": [],
                "Merge Sort por nome": [],
                "Insercao no Heap": [],
                "Remocao completa do Heap": []
            }

            for repeticao in range(REPETICOES):
                dados = criarDados(volume, cenario)

                def inserirTodos():
                    raiz_teste = None
                    for med in dados:
                        raiz_teste = inserir(raiz_teste, med)

                tempos["Insercao AVL"].append(medir(inserirTodos))

                raiz = construirArvore(dados)

                tempos["Busca por registro existente"].append(
                    medir(lambda: buscarRegistro(raiz, volume))
                )
                tempos["Busca por registro inexistente"].append(
                    medir(lambda: buscarRegistro(raiz, volume + 1))
                )

                nome_existente = f"Medicamento {volume:05d}"
                tempos["Busca por nome existente"].append(
                    medir(lambda: buscarNome(raiz, nome_existente))
                )
                tempos["Busca por nome inexistente"].append(
                    medir(lambda: buscarNome(raiz, "Medicamento inexistente"))
                )

                raiz_remocao = construirArvore(dados)
                tempos["Remocao AVL"].append(
                    medir(lambda: remover(raiz_remocao, volume))
                )

                tempos["Travessia em ordem"].append(
                    medir(lambda: emOrdem(raiz, []))
                )
                tempos["Travessia pre-ordem"].append(
                    medir(lambda: preOrdem(raiz, []))
                )
                tempos["Travessia pos-ordem"].append(
                    medir(lambda: posOrdem(raiz, []))
                )

                lista_ordenacao = []
                emOrdem(raiz, lista_ordenacao)
                tempos["Merge Sort por nome"].append(
                    medir(lambda: mergeSort(lista_ordenacao.copy()))
                )

                fila_base = dados.copy()
                def inserirTodosHeap():
                    fila = []
                    for med in fila_base:
                        inserirHeap(fila, med)
                tempos["Insercao no Heap"].append(medir(inserirTodosHeap))

                fila_remocao = []
                for med in dados:
                    inserirHeap(fila_remocao, med)

                def removerTodosHeap():
                    while fila_remocao:
                        removerHeap(fila_remocao)
                tempos["Remocao completa do Heap"].append(medir(removerTodosHeap))

            print(f"\nVolume: {volume} registros | Cenario: {cenario}")
            for operacao, lista_tempos in tempos.items():
                media = sum(lista_tempos) / len(lista_tempos)
                print(f"{operacao}: {media:.6f} ms")
                resultados.append([volume, cenario, operacao, f"{media:.6f}"])

    nome_arquivo = "resultados_benchmark_otimizado.csv"
    with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["Volume", "Cenario", "Operacao", "Media (ms)"])
        escritor.writerows(resultados)

    print(f"\nResultados salvos em: {nome_arquivo}")
    print("\nOBSERVACOES:")
    print("- A busca por nome percorre a AVL, pois a arvore esta ordenada por registro.")
    print("- Portanto, a busca por nome pode ser O(n), nao O(log n).")
    print("- As travessias medem a criacao da lista, sem impressao no terminal.")
    print("- O Merge Sort mede somente a ordenacao; a obtencao da lista fica fora do tempo.")
    print("- A remocao mede uma remocao individual; a arvore e montada antes do cronometro.")
    print("- O Heap mede a insercao de todos os itens e a remocao completa da fila.")


if __name__ == "__main__":
    benchmark()
