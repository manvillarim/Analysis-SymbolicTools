import matplotlib.pyplot as plt

# Ferramentas e pontuações fornecidas
tools = ["Halmos", "hevm", "kontrol"]

# Pontuações das ferramentas para cada peso
results_halmos = [100, 100, 100, 100, 100, 100, 0, 0]
results_hevm = [100, 93, 0, 0, 100, 85.7, 85.7, 0]
results_kontrol = [3.7, None, None, None, 6.4, None, None, None]

# Pesos das características
weights = [3, 6, 8, 10, 3, 4, 5, 9]

# Resultados das porcentagens para cada ferramenta
percentages = {
    "Halmos": results_halmos,
    "hevm": results_hevm,
    "kontrol": results_kontrol,
}


# Função para calcular os scores considerando pesos inversos
def calculate_score(percentages, weights):
    scores = {}
    total_weight = sum(weights)
    inverse_weights = [
        total_weight / w for w in weights
    ]  # Peso inverso para ajuste do impacto

    for tool, percents in percentages.items():
        score = 0
        total_inverse_weight = 0  # Soma dos pesos inversos para normalização

        for i, percent in enumerate(percents):
            if percent is not None:
                # Ajuste inverso (quanto menor o peso, maior o impacto do erro)
                score += (percent / 100) * inverse_weights[i]
                total_inverse_weight += inverse_weights[i]

        # Média ponderada ajustada
        scores[tool] = score / total_inverse_weight if total_inverse_weight > 0 else 0

    return scores


# Calcular os scores para cada ferramenta
scores = calculate_score(percentages, weights)


# Gráfico
def plot_scores(scores):
    labels = list(scores.keys())
    score_values = list(scores.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, score_values, color=["skyblue", "lightgreen", "lightcoral"])
    plt.title("Reliability Scores of Tools")
    plt.ylabel("Scores")
    plt.xlabel("Tools")
    plt.ylim([0, 1])  # A pontuação máxima é 1 (100%)
    plt.savefig("reliability_scores.pdf", format="pdf", bbox_inches="tight")
    plt.show()


# Exibindo os scores calculados
print("Scores calculados:")
for tool, score in scores.items():
    print(f"{tool}: {score:.2f}")

# Gerar o gráfico
plot_scores(scores)
