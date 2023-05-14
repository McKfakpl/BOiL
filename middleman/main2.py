from pulp import LpProblem, LpVariable, LpMaximize, lpSum, value

def optimize_middleman(ai, bj, kz, cj, ktij):
    # Inicjalizacja modelu optymalizacji
    problem = LpProblem("MiddlemanOptimization", LpMaximize)

    # Tworzenie zmiennych decyzyjnych
    x = []
    for i in range(len(ai)):
        x.append([])
        for j in range(len(bj)):
            x[i].append(LpVariable(f"x{i}{j}", lowBound=0))

    # Definiowanie funkcji celu
    problem += lpSum(cj[j] * x[i][j] for i in range(len(ai)) for j in range(len(bj))) \
               - lpSum(kz[i] * x[i][j] for i in range(len(ai)) for j in range(len(bj)))

    # Definiowanie ograniczeń podaży
    for i in range(len(ai)):
        problem += lpSum(x[i][j] for j in range(len(bj))) <= ai[i]

    # Definiowanie ograniczeń popytu
    for j in range(len(bj)):
        problem += lpSum(x[i][j] for i in range(len(ai))) <= bj[j]

    # Rozwiązanie problemu optymalizacji
    problem.solve()

    # Pobranie wyników
    status = problem.status
    total_cost = value(problem.objective)
    total_revenue = sum(cj[j] * value(x[i][j]) for i in range(len(ai)) for j in range(len(bj)))
    total_profit = total_revenue - total_cost

    return status, total_cost, total_revenue, total_profit


# Przykładowe dane
ai = [20, 30]  # Podaż dostawców
bj = [10, 28, 27]  # Popyt odbiorców
kz = [10,12]  # Koszt zakupu od dostawców
cj = [30, 25, 30]  # Cena sprzedaży odbiorcom
ktij = [
    [8, 14, 17],
    [12, 9, 19]
]  # Koszt transportu od dostaw

# Wywołanie optymalizacji
status, total_cost, total_revenue, total_profit = optimize_middleman(ai, bj, kz, cj, ktij)

# Wyświetlenie wyników
print("Status rozwiązania:", status)
print("Koszt całkowity:", total_cost)
print("Przychód całkowity:", total_revenue)
print("Zysk pośrednika:", total_profit)
