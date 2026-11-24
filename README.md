# Projeto ERP Farmácia — Farmácias Bahia

Sistema de controle de estoque de farmácia em Python (console), desenvolvido para a disciplina de **Algoritmos e Estruturas de Dados** (UNIFAN, 2026.2).

O repositório tem duas versões do sistema e os benchmarks que comparam o desempenho delas.

**Autores:** Levi Matheus, Vinicius Batista e Ezequiel Azevedo

## Estrutura

```
projeto-erp-farmacia/
├── farmacia-original/
│   └── Farmacia.py              # Versão base (TDE I): listas, insertion sort e busca binária
├── farmacia-otimizado/
│   └── Farmacia_Otimizado.py    # Versão otimizada (TDE II): AVL, Merge Sort e Heap
├── benchmarks/
│   ├── benchmark_original.py    # Mede a versão original
│   └── benchmark_otimizado.py   # Mede a versão otimizada (gera CSV)
└── README.md
```

## Versões do sistema

| | Original | Otimizada |
|---|---|---|
| Armazenamento | Lista | Árvore AVL (por nº de registro) |
| Ordenação por nome | Insertion Sort | Merge Sort |
| Alertas de validade | PriorityQueue | Heap implementado manualmente |

## Como executar

Requer **Python 3.12 ou superior** (o código usa aspas duplas dentro de f-strings).

```bash
# Sistema original
python farmacia-original/Farmacia.py

# Sistema otimizado
python farmacia-otimizado/Farmacia_Otimizado.py
```

## Benchmarks

Os benchmarks usam 3 volumes (100, 1.000 e 10.000 registros), 3 cenários (aleatório, ordenado e inverso) e 5 repetições por teste, exibindo a média em milissegundos.

```bash
python benchmarks/benchmark_original.py

python benchmarks/benchmark_otimizado.py
# gera resultados_benchmark_otimizado.csv na pasta onde for executado
```

> Observação: no benchmark otimizado, a busca por nome percorre a AVL inteira (a árvore é ordenada por registro), então pode ser O(n).
