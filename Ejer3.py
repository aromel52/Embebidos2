#EJERCICIO 3.
def obtener_informacion_usuario():
    nombre = input("¿Cuál es tu nombre? ")
    edad = input("¿Cuántos años tienes? ")
    profesion = input("¿Cuál es tu profesión? ")
    
    mensaje = f"Hola, {nombre}! Tienes {edad} años y trabajas como {profesion}."
    
    print(mensaje)

obtener_informacion_usuario()
