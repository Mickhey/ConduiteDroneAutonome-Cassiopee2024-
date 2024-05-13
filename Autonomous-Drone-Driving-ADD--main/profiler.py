import pstats

# Charger les statistiques
stats = pstats.Stats("output.prof")

# Trier et imprimer les statistiques
# Les options de tri incluent: 'calls', 'cumulative', 'line', 'name', 'nfl', 'time'
stats.sort_stats("cumulative").print_stats(10)  # Imprime les 10 résultats les plus significatifs basés sur le temps cumulatif
