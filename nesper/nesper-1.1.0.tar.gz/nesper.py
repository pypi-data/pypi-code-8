"""Esse é um módulo "nester.py" e fornece uma função chamada print_lol() que imprime listas que podem ou não conter listas aninhadas.Pequena modificação no comentário do arquivo"""
def print_lol(the_list, level):
	for i in the_list:
		if isinstance(i, list):
			print_lol(i, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end=")
			print(i)
