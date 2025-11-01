# ================================================================
# Gestão de Consumo em Unidades de Diagnóstico
# Disciplina: Dynamic Programming
# Código completo: funcionalidades originais + Programação Dinâmica
# ================================================================

from collections import deque
from functools import lru_cache

# ------------------------------
# Produtos disponíveis
# ------------------------------
produtos = [
    "reagente_X", "luvas", "máscaras", "seringas", "algodão",
    "tubos_coleta", "etiquetas", "álcool_gel", "gazes", "papel_laboratorio"
]

# ------------------------------
# Fila e consumo total
# ------------------------------
fila_consumo = []  # lista de registros: [produto, quantidade]
consumo_total = {p: 0 for p in produtos}  # soma total do consumo por produto

# ------------------------------
# Registrar consumo manual (adiciona à fila e atualiza consumo_total)
# ------------------------------
def registrar_consumo_manual():
    print("\n=== Registrar Consumo Diário ===")
    produto = escolher_produto()
    try:
        quantidade = int(input(f"Quantidade consumida de {produto}: "))
        # Adiciona ao final da lista (fila)
        fila_consumo.append([produto, quantidade])
        consumo_total[produto] += quantidade
        print(f"✅ Consumo registrado: {produto} - {quantidade}")
    except ValueError:
        print("Entrada inválida! Digite um número inteiro.")

# ------------------------------
# Exibir Fila (FIFO)
# ------------------------------
def mostrar_fila():
    print("\n=== Consumo em ordem cronológica (Fila) ===")
    if not fila_consumo:
        print("Nenhum consumo registrado ainda.")
    else:
        for i, (produto, qtd) in enumerate(fila_consumo, start=1):
            print(f"{i}. {produto} - {qtd}")

# ------------------------------
# Exibir Pilha (LIFO)
# ------------------------------
def mostrar_pilha():
    print("\n=== Consumo em ordem inversa (Pilha) ===")
    if not fila_consumo:
        print("Nenhum consumo registrado ainda.")
    else:
        for i in range(len(fila_consumo)-1, -1, -1):
            produto, qtd = fila_consumo[i]
            print(f"{len(fila_consumo)-i}. {produto} - {qtd}")

# ------------------------------
# Escolher produto
# ------------------------------
def escolher_produto():
    print("\nEscolha o produto pelo número:")
    for i, p in enumerate(produtos):
        print(f"{i + 1} - {p}")
    while True:
        try:
            escolha = int(input("Número do produto: "))
            if 1 <= escolha <= len(produtos):
                return produtos[escolha - 1]
            else:
                print("Número inválido, tente novamente.")
        except ValueError:
            print("Entrada inválida, digite um número.")

# ------------------------------
# Buscas: sequencial e binária
# ------------------------------
def busca_sequencial(produto_alvo):
    for i, p in enumerate(produtos):
        if p == produto_alvo:
            return i
    return -1

def busca_binaria(produto_alvo):
    lista_ordenada = sorted(produtos)
    left, right = 0, len(lista_ordenada) - 1
    while left <= right:
        mid = (left + right) // 2
        if lista_ordenada[mid] == produto_alvo:
            return mid
        elif lista_ordenada[mid] < produto_alvo:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# ------------------------------
# Ordenação por consumo total (descendente): merge sort e quick sort
# ------------------------------
def merge_sort(lista, consumo_total):
    if len(lista) <= 1:
        return lista[:]
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio], consumo_total)
    direita = merge_sort(lista[meio:], consumo_total)
    return merge(esquerda, direita, consumo_total)

def merge(esquerda, direita, consumo_total):
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if consumo_total[esquerda[i]] >= consumo_total[direita[j]]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado

def quick_sort(lista, consumo_total):
    if len(lista) <= 1:
        return lista[:]
    pivot = lista[0]
    maiores_ou_iguais = [x for x in lista[1:] if consumo_total[x] >= consumo_total[pivot]]
    menores = [x for x in lista[1:] if consumo_total[x] < consumo_total[pivot]]
    return quick_sort(maiores_ou_iguais, consumo_total) + [pivot] + quick_sort(menores, consumo_total)

# ------------------------------
# ---------- PROGRAMACAO DINAMICA ----------
# ------------------------------
# Objetivo: dado um horizonte de T dias com demanda (forecast) d_0..d_{T-1},
# decidir quantas unidades pedir em cada dia (q_t) para minimizar custos:
#  - custo de pedido fixo K (se q_t > 0)
#  - custo unitário de pedido c (por unidade pedida)
#  - custo de holding h (por unidade em estoque ao fim do dia)
#  - custo de shortage/ruptura p (por unidade de demanda não atendida)
#
# Estados:
#  - (t, s) onde t = dia atual (0..T) e s = estoque ao início do dia t (0..Smax)
#
# Decisões:
#  - q in [0..Smax - s] (quantidade a pedir no início do dia t). Pedido chega instantaneamente (modelo simples).
#
# Transição:
#  - s' = max(0, s + q - d_t)  (estoque no início do próximo dia)
#  - shortage = max(0, d_t - (s + q))
#
# Função objetivo (minimizar custo total):
#  cost(t, s, q) = (K if q>0 else 0) + c*q + p*shortage + h*s'
#
# Devemos implementar:
#  - recursiva pura (pode explodir em tempo)
#  - recursiva com memoização (top-down)
#  - iterativa bottom-up (tabular)
#
# Ao final, retornar custo mínimo e política (q_t por dia).
#
# Observação: para simplificar e para o escopo acadêmico, trabalhamos com quantidades inteiras e Smax razoável.
# ------------------------------

def forecast_demand(produto, T=7):
    """
    Gera uma previsão de demanda para os próximos T dias baseada no histórico.
    Estratégia simples:
      - Se houver registros para o produto, usa média dos últimos N registros.
      - Caso contrário, fallback para demanda = 1 por dia.
    """
    # extrair histórico só para o produto
    ultimos = [q for p, q in fila_consumo if p == produto]
    if not ultimos:
        return [1 for _ in range(T)]
    N = min(7, len(ultimos))
    mean = max(1, sum(ultimos[-N:]) // N)
    return [mean for _ in range(T)]

def dp_params_example():
    """
    Parâmetros padrão do modelo DP:
      K: custo fixo por pedido
      c: custo unitário por unidade pedida
      h: custo de armazenagem por unidade por dia (holding)
      p: custo de penalidade por unidade não atendida (shortage)
      Smax: estoque máximo considerado no estado
    """
    return {"K": 20.0, "c": 2.0, "h": 0.5, "p": 10.0, "Smax": 50}

# ------------------------------
# Recursiva pura (exponencial)
# ------------------------------
def dp_recursive(demand, params):
    T = len(demand)
    K, c, h, p, Smax = params["K"], params["c"], params["h"], params["p"], params["Smax"]

    def rec(t, s):
        # retorna (custo_min, politica_list) do estado (t, s)
        if t == T:
            return 0.0, []  # sem custo ao final
        best_cost = float('inf')
        best_policy = None
        # decidir quantidade q para pedir hoje (0..Smax - s)
        for q in range(Smax - s + 1):
            pedido_cost = (K if q > 0 else 0.0) + c * q
            disponivel = s + q
            shortage = max(0, demand[t] - disponivel)
            s_next = max(0, disponivel - demand[t])
            holding_cost = h * s_next
            day_cost = pedido_cost + p * shortage + holding_cost
            future_cost, future_pol = rec(t + 1, s_next)
            total_cost = day_cost + future_cost
            if total_cost < best_cost:
                best_cost = total_cost
                best_policy = [q] + future_pol
        return best_cost, best_policy

    return rec(0, 0)  # iniciando no dia 0 com estoque 0

# ------------------------------
# Recursiva com memoização (top-down)
# ------------------------------
def dp_memoized(demand, params):
    T = len(demand)
    K, c, h, p, Smax = params["K"], params["c"], params["h"], params["p"], params["Smax"]

    @lru_cache(maxsize=None)
    def rec(t, s):
        if t == T:
            return (0.0, ())  # política como tupla
        best_cost = float('inf')
        best_policy = None
        for q in range(Smax - s + 1):
            pedido_cost = (K if q > 0 else 0.0) + c * q
            disponivel = s + q
            shortage = max(0, demand[t] - disponivel)
            s_next = max(0, disponivel - demand[t])
            holding_cost = h * s_next
            day_cost = pedido_cost + p * shortage + holding_cost
            future_cost, future_pol = rec(t + 1, s_next)
            total_cost = day_cost + future_cost
            if total_cost < best_cost:
                best_cost = total_cost
                best_policy = (q,) + future_pol
        return best_cost, best_policy

    cost, policy_tuple = rec(0, 0)
    return cost, list(policy_tuple)

# ------------------------------
# Iterativa bottom-up (tabular)
# ------------------------------
def dp_bottom_up(demand, params):
    T = len(demand)
    K, c, h, p, Smax = params["K"], params["c"], params["h"], params["p"], params["Smax"]
    # dp[t][s] = minimal cost from day t with inventory s
    dp = [[float('inf')] * (Smax + 1) for _ in range(T + 1)]
    decision = [[0] * (Smax + 1) for _ in range(T)]
    # base: t == T => cost 0 for all s
    for s in range(Smax + 1):
        dp[T][s] = 0.0

    # iterar t de T-1 até 0
    for t in range(T - 1, -1, -1):
        for s in range(Smax + 1):
            best_cost = float('inf')
            best_q = 0
            for q in range(Smax - s + 1):
                pedido_cost = (K if q > 0 else 0.0) + c * q
                disponivel = s + q
                shortage = max(0, demand[t] - disponivel)
                s_next = max(0, disponivel - demand[t])
                holding_cost = h * s_next
                day_cost = pedido_cost + p * shortage + holding_cost
                total_cost = day_cost + dp[t + 1][s_next]
                if total_cost < best_cost:
                    best_cost = total_cost
                    best_q = q
            dp[t][s] = best_cost
            decision[t][s] = best_q

    # reconstruir política a partir de estado inicial (0, s=0)
    s = 0
    policy = []
    for t in range(T):
        q = decision[t][s]
        policy.append(q)
        disponivel = s + q
        s = max(0, disponivel - demand[t])
    return dp[0][0], policy

# ------------------------------
# Função utilitária: roda os 3 métodos e compara resultados
# ------------------------------
def run_dp_for_product_interactive():
    produto = escolher_produto()
    try:
        T = int(input("Horizonte (dias) para planejamento (ex: 7): "))
        if T <= 0:
            print("Valor inválido de dias; usando T=7.")
            T = 7
    except ValueError:
        T = 7

    # gerar forecast interativo: usar histórico (média) ou inserir manualmente
    use_hist = input("Usar forecast automático a partir do histórico? (s/n) ").strip().lower()
    if use_hist in ("s", "sim"):
        demand = forecast_demand(produto, T=T)
    else:
        print("Insira a demanda prevista para cada dia. Deixe em branco para usar 1.")
        demand = []
        for i in range(T):
            v = input(f"Demanda prevista dia {i+1}: ").strip()
            if v == "":
                demand.append(1)
            else:
                try:
                    demand.append(int(v))
                except ValueError:
                    print("Entrada inválida, usando 1.")
                    demand.append(1)

    params = dp_params_example()
    custom = input("Deseja ajustar parâmetros de custo? (s/n): ").strip().lower()
    if custom in ("s", "sim"):
        try:
            params["K"] = float(input(f"Custo fixo por pedido K (atual {params['K']}): ") or params["K"])
            params["c"] = float(input(f"Custo por unidade c (atual {params['c']}): ") or params["c"])
            params["h"] = float(input(f"Holding por unidade h (atual {params['h']}): ") or params["h"])
            params["p"] = float(input(f"Penalty por falta p (atual {params['p']}): ") or params["p"])
            params["Smax"] = int(input(f"Estoque máximo Smax (atual {params['Smax']}): ") or params["Smax"])
        except ValueError:
            print("Entrada inválida em parâmetros, usando valores padrão.")

    print(f"\nRodando DP para '{produto}' por {T} dias.")
    print(f"Demanda prevista (dias 0..{T-1}): {demand}")
    print(f"Parâmetros: K={params['K']}, c={params['c']}, h={params['h']}, p={params['p']}, Smax={params['Smax']}")

    # recursiva pura (cuidado: lento quando Smax*T grande)
    cost_rec, policy_rec = dp_recursive(demand, params)
    # memoizada
    cost_mem, policy_mem = dp_memoized(demand, params)
    # bottom-up
    cost_bot, policy_bot = dp_bottom_up(demand, params)

    eps = 1e-6
    same_costs = abs(cost_rec - cost_mem) < eps and abs(cost_mem - cost_bot) < eps
    same_policies = (policy_rec == policy_mem == policy_bot)

    print("\n--- Resultados ---")
    print(f"Recursiva pura: custo={cost_rec:.2f}, política={policy_rec}")
    print(f"Memoizada     : custo={cost_mem:.2f}, política={policy_mem}")
    print(f"Bottom-up     : custo={cost_bot:.2f}, política={policy_bot}")
    print(f"\nVerificação de igualdade de custos: {'OK' if same_costs else 'DIFERENTES'}")
    print(f"Verificação de igualdade de políticas: {'OK' if same_policies else 'POSSIVELMENTE DIFERENTES'}")
    if not same_policies:
        print("Obs: políticas podem diferir quando custos empatam; confirme com análise adicional.")

    input("\nPressione ENTER para voltar ao menu...")

# ------------------------------
# Menu principal (com todas as opções)
# ------------------------------
def menu():
    while True:
        print("\n--- Menu ---")
        print("1 - Registrar consumo diário (Fila)")
        print("2 - Ver consumo em ordem cronológica (Fila)")
        print("3 - Ver consumo em ordem inversa (Pilha)")
        print("4 - Busca sequencial por produto")
        print("5 - Busca binária por produto")
        print("6 - Produtos ordenados por consumo total (merge sort)")
        print("7 - Produtos ordenados por consumo total (quick sort)")
        print("8 - Rodar Programação Dinâmica (previsão + política de pedidos)")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar_consumo_manual()
        elif opcao == "2":
            mostrar_fila()
        elif opcao == "3":
            mostrar_pilha()
        elif opcao == "4":
            produto_alvo = escolher_produto()
            idx = busca_sequencial(produto_alvo)
            if idx != -1:
                print(f"Produto '{produto_alvo}' encontrado na posição {idx} na lista de produtos.")
            else:
                print(f"Produto '{produto_alvo}' não encontrado.")
        elif opcao == "5":
            produto_alvo = escolher_produto()
            idx = busca_binaria(produto_alvo)
            if idx != -1:
                print(f"Produto '{produto_alvo}' encontrado na lista ordenada de produtos na posição {idx}.")
            else:
                print(f"Produto '{produto_alvo}' não encontrado.")
        elif opcao == "6":
            ordenados_merge = merge_sort(produtos[:], consumo_total)
            print("\nProdutos ordenados por consumo total (merge sort):")
            for p in ordenados_merge:
                print(f"{p} - Consumo total: {consumo_total[p]}")
        elif opcao == "7":
            ordenados_quick = quick_sort(produtos[:], consumo_total)
            print("\nProdutos ordenados por consumo total (quick sort):")
            for p in ordenados_quick:
                print(f"{p} - Consumo total: {consumo_total[p]}")
        elif opcao == "8":
            run_dp_for_product_interactive()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

# ------------------------------
# Inicialização
# ------------------------------
if __name__ == "__main__":
    print("Iniciando sistema de gestão de consumo...")
    menu()
