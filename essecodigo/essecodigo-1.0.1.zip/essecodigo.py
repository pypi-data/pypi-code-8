''' esta função serve para imprimir uma lista que esta dentro de outra lista e
precisa ser chamada uma só ver por lista mais externa'''

def print_lista(insira_a_lista_aqui):

    '''para cada objeto da lista adicionada como parametro da função sera analizado
    para verificar se é uma lista interna ou não e imprimir o resultado'''
    
    for lista in insira_a_lista_aqui:
        if isinstance(lista , list):
           print_lista(lista)
        else: print(lista)
