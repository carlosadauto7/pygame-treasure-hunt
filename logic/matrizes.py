from random import randint

def matriz(tamanho):
    matriz1 = [[0]*tamanho for i in range(tamanho)]
    return matriz1

def tesouros(matriz):
    num_tesouros = 0

    while num_tesouros <= 0.32*(len(matriz)**2):
        i = randint(0, len(matriz)-1)
        j = randint(0, len(matriz)-1)
        if(matriz[i][j] != 'T'):
            matriz[i][j] = 'T'
            num_tesouros += 1

    return (matriz, num_tesouros)

def buraco(matriz):
    num_buracos = 0
    while num_buracos <= 0.13*(len(matriz)**2):
        i = randint(0, len(matriz)-1)
        j = randint(0, len(matriz)-1)
        if matriz[i][j] != 'T' and matriz[i][j] != 'B':
            matriz[i][j] = 'B'
            num_buracos += 1
    return (matriz, num_buracos)

def contar_tesouros(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            valor = matriz[i][j]
            if(valor == 'T'):
                if(i == 0 and j == 0):
                    if(type(matriz[i+1][j]) == int):
                        matriz[i+1][j] += 1
                    if(type(matriz[i][j+1]) == int):
                        matriz[i][j+1] += 1
                elif(i == 0 and j != len(matriz) - 1):
                    if(type(matriz[i+1][j]) == int):
                        matriz[i+1][j] += 1
                    if(type(matriz[i][j+1]) == int):
                        matriz[i][j+1] += 1
                    if(type(matriz[i][j-1]) == int):
                        matriz[i][j-1] += 1
                elif(i != len(matriz)-1 and j == 0):
                    if(type(matriz[i+1][j]) == int):
                        matriz[i+1][j] += 1
                    if(type(matriz[i][j+1]) == int):
                        matriz[i][j+1] += 1
                    if(type(matriz[i-1][j]) == int):
                        matriz[i-1][j] += 1
                elif(i == len(matriz) - 1 and j == len(matriz) -1):
                    if(type(matriz[i-1][j]) == int):
                        matriz[i-1][j] += 1
                    if(type(matriz[i][j-1]) == int):
                        matriz[i][j-1] += 1
                elif(i == len(matriz) - 1 and j != 0):
                    if(type(matriz[i-1][j]) == int):
                        matriz[i-1][j] += 1
                    if(type(matriz[i][j+1]) == int):
                        matriz[i][j+1] += 1
                    if(type(matriz[i][j-1]) == int):
                        matriz[i][j-1] += 1
                elif(i != 0 and j == len(matriz) - 1):
                    if(type(matriz[i-1][j]) == int):
                        matriz[i-1][j] += 1
                    if(type(matriz[i][j-1]) == int):
                        matriz[i][j-1] += 1
                    if(type(matriz[i+1][j]) == int):
                        matriz[i+1][j] += 1
                elif(i == len(matriz) - 1 and j == 0):
                    if(type(matriz[i-1][j]) == int):
                        matriz[i-1][j] += 1
                    if(type(matriz[i][j+1]) == int):
                        matriz[i][j+1] += 1
                elif(i == 0 and j == len(matriz) - 1):
                    if(type(matriz[i+1][j]) == int):
                        matriz[i+1][j] += 1
                    if(type(matriz[i][j-1]) == int):
                        matriz[i][j-1] += 1
                else:
                    if(type(matriz[i+1][j]) == int):
                        matriz[i+1][j] += 1
                    if(type(matriz[i][j-1]) == int):
                        matriz[i][j-1] += 1
                    if(type(matriz[i-1][j]) == int):
                        matriz[i-1][j] += 1
                    if(type(matriz[i][j+1]) == int):
                        matriz[i][j+1] += 1
    return matriz
        
def matriz_geral(tamanho):
    matrizz = contar_tesouros(buraco(tesouros(matriz(tamanho))[0])[0])
    for i in range(len(matrizz)):
        for j in range(len(matrizz)):
            matrizz[i][j] = str(matrizz[i][j])
    return matrizz

def count(matriz):
    num_bur = buraco(matriz)[1]
    num_tes = tesouros(matriz)[1]
    return (num_tes, num_bur)

def main():
    n = 7
    matriz = matriz_geral(n)
    for linha in matriz:
        print(linha)

if __name__ == '__main__':
    main()