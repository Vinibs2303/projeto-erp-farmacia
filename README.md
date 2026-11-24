# Projeto ERP Farmácia — Farmácias Bahia

Sistema de controle de estoque de farmácia em Python (console), desenvolvido para a disciplina de **Algoritmos e Estruturas de Dados** (UNIFAN, 2026.2).

O repositório tem duas versões do sistema.

**Autores:** Levi Matheus, Vinicius Batista e Ezequiel Azevedo

## Estrutura

```
projeto-erp-farmacia/
├── farmacia-original/
│   └── Farmacia.py              # Versão base (TDE I): listas, insertion sort e busca binária
├── farmacia-otimizado/
│   └── Farmacia_Otimizado.py    # Versão otimizada (TDE II): AVL, Merge Sort e Heap
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
