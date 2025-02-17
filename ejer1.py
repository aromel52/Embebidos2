def suma_numeros():
    n = int(input("n"))
    suma = 0
    for i in range(n):
        num = float(input(f"Ingresar"))
        suma += num
    return suma
resultado = suma_numeros()
print("r", resultado)