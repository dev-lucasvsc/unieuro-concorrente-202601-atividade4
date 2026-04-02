# Benchmark de Paralelismo com Multiprocessing em Python

**Disciplina:** Programação Concorrente e Distribuída  
**Aluno:** Lucas Vasconcelos Pessoa de Oliveira  
**Turma:** ADSN04  
**Professor:** Rafael  
**Data:** 01/04/2026  

---

## 1. Descrição do Problema

O programa foi feito pra processar uma **imagem PPM de ~16 GB** em paralelo, dividindo o trabalho entre vários processos ao mesmo tempo pra ver se fica mais rápido.

A imagem é dividida em partes horizontais iguais. Cada parte é convertida individualmente para escala de cinza usando a fórmula de luminância padrão. No final, todas as partes são reunidas em uma única imagem de saída.

| Pergunta | Resposta |
|----------|----------|
| Objetivo | Converter uma imagem PPM de ~16 GB para escala de cinza em paralelo e comparar os tempos |
| Volume de dados | Imagem 75672x75672 pixels — ~16 GB — dividida em 12 partes |
| Algoritmo | Divisão horizontal da imagem + processamento paralelo com `multiprocessing.Pool.map()` chamando `conversoremescalacinza.py` como subprocesso |
| Complexidade | O(N/p) — quanto mais processos, menos pixels por processo |

---

## 2. Ambiente Experimental

| Item | Descrição |
|------|-----------|
| Processador | 12th Gen Intel Core i7-12700 — 2.10 GHz |
| Número de núcleos | 12 núcleos físicos / 20 threads lógicas |
| Memória RAM | 16,0 GB (utilizável: 15,7 GB) |
| Sistema Operacional | Windows 11 — 64 bits |
| Linguagem utilizada | Python 3.13 |
| Biblioteca de paralelização | `multiprocessing` (já vem com o Python) |
| Compilador / Versão | CPython 3.13 |

---

## 3. Metodologia de Testes

O tempo foi medido usando `time.time()`, contando o tempo total do processamento paralelo — da criação dos processos até a conclusão de todas as partes.

Cada configuração foi rodada **1 vez**, com a pasta `partes_cinza/` limpa antes de cada execução para garantir que os resultados não fossem influenciados por arquivos já existentes.

### Configurações testadas

- 1 processo
- 2 processos
- 4 processos
- 8 processos
- 12 processos

---

## 4. Resultados Experimentais

| Nº Processos | Tempo de Execução (s) |
|:------------:|:---------------------:|
| 1            | 155.87                |
| 2            | 101.47                |
| 4            | 87.61                 |
| 8            | 93.72                 |
| 12           | 88.40                 |

---

## 5. Cálculo de Speedup e Eficiência

O **speedup** mostra quantas vezes ficou mais rápido em relação ao tempo sem paralelismo:

```
Speedup(p) = T(1) / T(p)
```

A **eficiência** mostra se os processos estão sendo bem aproveitados (1,0 seria o ideal):

```
Eficiência(p) = Speedup(p) / p
```

---

## 6. Tabela de Resultados

| Processos | Tempo (s) | Speedup | Eficiência |
|:---------:|:---------:|:-------:|:----------:|
| 1         | 155.87    | 1.00    | 1.00       |
| 2         | 101.47    | 1.54    | 0.77       |
| 4         | 87.61     | 1.78    | 0.45       |
| 8         | 93.72     | 1.66    | 0.21       |
| 12        | 88.40     | 1.76    | 0.15       |

> **Melhor resultado: 4 processos (87.61s)**

---

## 7. Análise dos Resultados

O ganho de desempenho foi modesto comparado ao ideal teórico. Com 2 processos houve uma melhora de 1.54x, e com 4 processos chegou ao melhor resultado (1.78x). A partir daí, aumentar o número de processos não trouxe ganho adicional — com 8 e 12 processos o tempo até piorou levemente em relação a 4.

O principal fator limitante nesse experimento é o **gargalo de I/O em disco**. Como a imagem tem ~16 GB, todos os processos precisam ler e escrever grandes volumes de dados simultaneamente, gerando contenção no acesso ao armazenamento. Diferente de workloads puramente computacionais, aqui o disco é o gargalo — não a CPU.

A eficiência caiu rapidamente com o aumento de processos (de 0.77 com 2 processos para 0.15 com 12), confirmando que o overhead de I/O supera o ganho de paralelismo a partir de um certo ponto.

**Principais fatores limitantes:**
- Contenção de I/O — múltiplos processos lendo/escrevendo no mesmo disco simultaneamente
- Overhead de criação e gerenciamento dos subprocessos
- Memória RAM limitada para buffers simultâneos de leitura

---

## 8. Conclusão

O paralelismo trouxe ganho moderado de desempenho, reduzindo o tempo de 155.87s para 87.61s com 4 processos (speedup de 1.78x).

O ganho não foi linear porque o gargalo principal é o acesso ao disco, não a capacidade de processamento da CPU. Para workloads com I/O intensivo em arquivos muito grandes, o ganho com paralelismo é limitado — o ponto ótimo foi 4 processos, após o qual a contenção de disco anulou os benefícios adicionais.

**Melhorias futuras:**
- Usar SSD NVMe para reduzir o gargalo de I/O
- Processar os pixels em memória sem escrita intermediária em disco
- Executar múltiplas vezes e calcular média para maior confiabilidade dos resultados
- Testar com `ProcessPoolExecutor` do `concurrent.futures` para comparação
