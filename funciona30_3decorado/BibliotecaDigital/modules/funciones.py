import random

import matplotlib.pyplot as plt

# def cargar_peli_desde_archivo(nombre_archivo, lista_pelis):
#     """Función que lee la información de los libros desde un archivo
#     y lo carga a una lista.
#     """
#     with open(nombre_archivo, "r") as archi:
#         for linea in archi:
#             frase,pelicula = linea.rstrip().split(';')
#             agregar_peli_a_lista(lista_pelis, frase, pelicula) 
#     return lista_pelis

def guardar_peli_en_archivo(nombre_archivo,frase,pelicula): 
    """Guarda la información de un libro en archivo
    """   
    with open(nombre_archivo, "a") as archi:
        archi.write(f"{frase},{pelicula}\n")
        
def seleccionar_opciones(pelicula_correcta, lista_pelis):
    opciones = [pelicula_correcta]
    while len(opciones) < 3:
        pelicula_opcion = random.choice(lista_pelis)["pelicula"]
        if pelicula_opcion not in opciones:
            opciones.append(pelicula_opcion)
    random.shuffle(opciones)
    return opciones

def seleccionar_frase_y_opciones(lista_pelis):
    frase_seleccionada = random.choice(lista_pelis)
    opciones = seleccionar_opciones(frase_seleccionada["pelicula"], lista_pelis)
    return frase_seleccionada, opciones

def verificar_respuesta(pelicula_ingresada, pelicula_correcta):
    return pelicula_ingresada.lower() == pelicula_correcta.lower()

def obtener_peliculas(lista_pelis):
    """Obtiene la lista de películas a partir de una lista de frases."""
    #lista_pelicul=[]
    peliculas = set()
    for frase, pelicula in lista_pelis:
        peliculas.add(pelicula)
        #lista_pelicul.append(z)
        return peliculas

def encontrar_pelicula_correcta(frase_seleccionada, opciones):
    pelicula_correcta = frase_seleccionada["pelicula"]
    
    # Itera sobre cada opción y verifica si coincide con la película correcta
    for opcion in opciones:
        if opcion == pelicula_correcta:
            return opcion
    
    # Si no se encuentra la película correcta, devuelve None
    return None

def obtener_peliculas(lista_pelis):
    """Obtiene la lista de películas a partir de una lista de frases."""
    #lista_pelicul=[]
    peliculas = set()
    for frase, pelicula in lista_pelis:
        peliculas.add(pelicula)
        #lista_pelicul.append(z)
    return sorted(peliculas)


def obtener_frase_y_opciones(lista_pelis, peliculas):
    frases = set(frase for frase, _ in lista_pelis)  # Usamos un nombre de variable diferente aquí
    frase_aleatoria = random.choice(list(frases))  # Cambiamos el nombre de la variable a frase_aleatoria
    pelicula_correcta = next(pelicula for frase, pelicula in lista_pelis if frase == frase_aleatoria)  # Usamos el nuevo nombre de variable
    
    opciones = [pelicula for pelicula in peliculas if pelicula != pelicula_correcta]
    if len(opciones) < 2:
        raise ValueError("No hay suficientes opciones disponibles")
    
    opciones_aleatorias = random.sample(opciones, 2)
    opciones_aleatorias.append(pelicula_correcta)
    random.shuffle(opciones_aleatorias)
    
    return frase_aleatoria, opciones_aleatorias, pelicula_correcta
