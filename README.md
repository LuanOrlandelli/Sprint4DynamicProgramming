# SPRINT 4 DYNAMIC PROGRAMMING

## 📋 Contexto do Problema

Nas unidades de diagnóstico da DASA, o consumo diário de insumos (como reagentes e descartáveis) não é registrado com precisão, dificultando o controle de estoque e a previsão de reposição.  

O encarregado precisa acessar o sistema **SAP** manualmente e registrar as saídas quando há tempo disponível, o que causa **baixa visibilidade** sobre o uso real de materiais.  

Como resultado, ocorrem:
- Falta de materiais essenciais;
- Excesso de estoque e aumento de custos;
- Falhas no planejamento de compras.

Este projeto propõe uma **solução computacional baseada em Programação Dinâmica** para **melhorar a visibilidade do consumo e reduzir desperdícios**.

---

## ⚙️ Funcionalidades Principais

O sistema permite:
1. Registrar o consumo diário de materiais (Fila).
2. Visualizar o consumo em ordem cronológica (FIFO) ou inversa (Pilha/LIFO).
3. Buscar produtos por nome usando busca **sequencial** e **binária**.
4. Ordenar produtos por consumo total com **Merge Sort** e **Quick Sort**.
5. Aplicar **Programação Dinâmica (DP)** para prever a demanda e determinar uma política de pedidos que minimize custos operacionais.

---

## 🧩 Estruturas e Algoritmos Utilizados

### 🔸 Estruturas de Dados
- **Fila (`list`)**: Armazena o consumo em ordem cronológica, simulando a sequência de uso diário dos insumos (modelo FIFO).
- **Pilha (`list`)**: Permite visualizar o consumo em ordem inversa, útil para revisar os últimos registros inseridos (modelo LIFO).
- **Dicionário (`dict`)**: Mantém o consumo total de cada produto acumulado ao longo do tempo.

Essas estruturas modelam o comportamento real do controle de estoque hospitalar, onde os itens são consumidos e repostos continuamente.

---

### 🔹 Algoritmos de Busca

#### 1. **Busca Sequencial**
Percorre toda a lista de produtos até encontrar o item desejado.  
Foi usada como **modelo simples** para simular buscas diretas no cadastro de materiais.

#### 2. **Busca Binária**
Opera sobre a lista **ordenada alfabeticamente**, reduzindo o tempo de busca de `O(n)` para `O(log n)`.  
Representa uma **melhoria no desempenho** do sistema de pesquisa interna.

---

### 🔹 Algoritmos de Ordenação

#### 1. **Merge Sort**
Algoritmo estável e eficiente (`O(n log n)`) usado para **ordenar produtos por consumo total** de forma recursiva (divisão e conquista).

#### 2. **Quick Sort**
Implementa a mesma ordenação com estratégia diferente (pivot e partição).  
Permite comparar **desempenho e comportamento prático** entre os dois algoritmos no mesmo contexto.

---

### 🔹 Programação Dinâmica (Coração do Projeto)

A **Programação Dinâmica (DP)** foi usada para **modelar o problema de decisão de estoque ótimo**.

#### ⚙️ Objetivo
Minimizar o custo total de operação ao longo de `T` dias, considerando:
- **Custo fixo de pedido (K)**  
- **Custo unitário de compra (c)**  
- **Custo de armazenagem (h)**  
- **Custo de falta (p)**  

#### 📦 Estados
- `(t, s)` onde:  
  `t` = dia atual  
  `s` = estoque disponível no início do dia `t`

#### 🎯 Decisões
- `q`: quantidade a pedir no início do dia `t`.

#### 🔁 Transição
- `s' = max(0, s + q - d_t)`  
  (estoque ao início do próximo dia)  
- `shortage = max(0, d_t - (s + q))`

#### 💰 Função Objetivo
- `custo_total = (K se q>0) + cq + hs' + p*shortage`
  O algoritmo busca a **política ótima de pedidos** `q_t` que minimize o custo acumulado ao longo dos dias.

---

### 🔸 Versões Implementadas

#### 1. **Recursiva Pura**
Implementa a DP de forma direta, recalculando subproblemas a cada chamada.  
→ Útil para **entender a formulação conceitual**.

#### 2. **Recursiva com Memoização (Top-Down)**
Adiciona cache de resultados para evitar recomputações.  
→ Reduz drasticamente o tempo de execução.  
→ Mostra o uso clássico de DP com **armazenamento de estados**.

#### 3. **Iterativa (Bottom-Up)**
Calcula de forma tabular, preenchendo todas as combinações possíveis de `(t, s)`.  
→ Representa a forma **eficiente e escalável** do algoritmo.

As três abordagens produzem o **mesmo resultado final**, validando a correção da modelagem.

---

## 📊 Resultados Esperados

- Melhoria na **precisão do controle de consumo**;  
- Possibilidade de **prever estoques críticos**;  
- Redução de **custos operacionais e desperdícios**;  
- Modelo escalável para outras unidades da rede.

---

## 🧠 Conclusão

Este projeto mostra como **estruturas de dados clássicas** e **algoritmos de busca, ordenação e otimização** podem ser aplicados a um problema **real de logística hospitalar**.  

A Programação Dinâmica permite **tomar decisões inteligentes de reposição de estoque**, garantindo equilíbrio entre custo e disponibilidade, ao mesmo tempo em que melhora a **visibilidade e eficiência operacional**.

---

## 👥 Equipe

**Grupo:**  
- Luan Orlandelli Ramos (554747)  
- Jorge Luiz Silva Santos (554418)  
- Arthur Albuquerque Menezes (562950)
- Arthur Bobadilla Franchi (555056)  
- Caio Rasuck Barbosa (93645)

**Disciplina:** Dynamic Programming  
**Instituição:** Faculdade de Informática e Administração Paulista  

