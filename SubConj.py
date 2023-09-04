def sub_conj(conjunto, subconjunto_actual, indice):
	if indice == len(conjunto):
		print(subconjunto_actual)
		return
	# Incluir el elemento actual en el subconjunto
	subconjunto_actual.append(conjunto[indice])
	sub_conj(conjunto, subconjunto_actual, indice + 1)
	# Excluir el elemento actual del subconjunto
	subconjunto_actual.pop()
	sub_conj(conjunto, subconjunto_actual, indice + 1)