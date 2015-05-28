''' esta função serve para imprimir uma lista que esta dentro de outra lista e
precisa ser chamada uma só ver por lista mais externa'''

def print_lista(insira_a_lista_aqui,tabulações):

    '''para cada objeto da lista adicionada como argumento da função sera analizado
    para verificar se é uma lista interna ou não e imprimir o resultado, e o argumento
    tabulações é a quantidade que você deseja para tabular as informações.'''
    
    for lista in insira_a_lista_aqui:
        if isinstance(lista , list):
           print_lista(lista, tabulações)
        else:
            for parar in range(tabulações):
                print('\t')
            print(lista)
