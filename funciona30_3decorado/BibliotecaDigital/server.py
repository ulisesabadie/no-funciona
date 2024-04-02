from flask import render_template, request, redirect, url_for, session
from modules.config import app
from modules.funciones import verificar_respuesta, seleccionar_frase_y_opciones, guardar_peli_en_archivo, obtener_peliculas, encontrar_pelicula_correcta, obtener_frase_y_opciones
import random
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64



#RUTA = "./data/"
ARCHIVO = r"C:\Users\Usuario\OneDrive\Escritorio\nay\no-funciona\funciona30_3decorado\BibliotecaDigital\data\frases_de_peliculas.txt"

lista_pelis = []  # Lista auxiliar
with open(ARCHIVO, "r", encoding="UTF-8") as archivo:
    for linea in archivo:
        lista_pelis.append(linea.split(";"))
# try:
#     cargar_peli_desde_archivo(ARCHIVO, lista_pelis)
# except FileNotFoundError:
#     with open(ARCHIVO, "w") as archi:
#         pass


@app.route("/", methods=["GET", "POST"])
def inicio():
    #global num_intentos
    if request.method == "POST":
        session["num_intentos"] = int(request.form["num_intentos"])
        session["usuario"] = request.form["usuario"]
        session["frases_previas"] = []
        session["aciertos"] = 0
        if session["num_intentos"] >= 3:
            frases_seleccionadas = random.sample(lista_pelis, session["num_intentos"])
            return redirect(url_for("jugar", frases_seleccionadas=frases_seleccionadas))
        else:
            mensaje = "El número mínimo son 3."
            return render_template("jugar.html", mensaje=mensaje)
    else:
        return render_template("inicio.html")

@app.route("/introduccion", methods=["POST"])
def introduccion():
    if request.method == "POST":
            return render_template("jugar.html")
    return redirect(url_for("inicio"))


resultados = []

@app.route("/jugar", methods=["GET", "POST"])
def jugar():
    if request.method == "POST":
        num_intentos = session["num_intentos"]
        if session["cont"] >= session["num_intentos"] - 1:
            # Juego completado, actualizar la sesión con la información necesaria
            session["nombre"] = session.get("usuario")
            session["hora_jugado"] = datetime.now().strftime("%H:%M:%S")
            session["aciertos"] = session.get("aciertos", 0)
            session["puntaje"] = f"{session['aciertos']}/{session['num_intentos']}"
            resultados.append({"nombre": session["nombre"], "puntaje": session["puntaje"], "hora": session["hora_jugado"]})
            return redirect(url_for("resultado_personal"))
        
        peliculas = obtener_peliculas(lista_pelis)
        frase, opciones_mezcladas, pelicula_correcta = obtener_frase_y_opciones(lista_pelis, peliculas)
        session["frase"] = frase
        session["opciones_mezcladas"] = opciones_mezcladas
        session["pelicula_correcta"] = pelicula_correcta
        session["cont"] += 1
        
        return render_template("jugar.html", num_intentos=session["num_intentos"], frase=frase, opciones=opciones_mezcladas, pelicula_correcta=pelicula_correcta)

    session["cont"] = 0  
    peliculas = session.get("opciones", [])  # Si opciones es None, se asigna una lista vacía
    frase = session.get("frase", "")  # Obtiene la frase de la sesión o establece una cadena vacía si no está presente
    opciones_mezcladas = session.get("opciones_mezcladas", [])  # Obtiene las opciones mezcladas de la sesión o establece una lista vacía si no está presente
    pelicula_correcta = session.get("pelicula_correcta", "")  # Obtiene la película correcta de la sesión o establece una cadena vacía si no está presente
    return render_template("jugar.html", num_intentos=session["num_intentos"], frase=frase, opciones=opciones_mezcladas, pelicula_correcta=pelicula_correcta)

@app.route("/mensaje", methods=["POST"])
def mensaje():
    opcion_seleccionada = request.form.get("respuesta")
    pelicula_correcta = session.get("pelicula_correcta")
    if pelicula_correcta == opcion_seleccionada:
        mensaje = "¡Correcto!"
    else:
        mensaje = f"¡Incorrecto! La respuesta correcta era: {pelicula_correcta}"

    

    # opcion_seleccionada = request.form.get("respuesta").lower()
    # pelicula_correcta = session.get("pelicula_correcta").lower()
    # if str(pelicula_correcta) == str(opcion_seleccionada):
    #     mensaje = "¡Correcto!"
    # else:
    #     mensaje = f"¡Incorrecto! La respuesta correcta era: {pelicula_correcta}"

    # Borra la frase, opciones y película correcta de la sesión para generar una nueva en el próximo juego
    session.pop("frase", None)
    session.pop("opciones", None)
    session.pop("pelicula_correcta", None)

    #Genera una nueva frase y opciones para el próximo juego
    peliculas = obtener_peliculas(lista_pelis)
    frase, opciones, pelicula_correcta = obtener_frase_y_opciones(lista_pelis, peliculas)
    session["frase"] = frase
    session["opciones"] = opciones
    session["pelicula_correcta"] = pelicula_correcta

    return render_template("mensaje.html", mensaje=mensaje, opcion_seleccionada=opcion_seleccionada, pelicula_correcta=pelicula_correcta)

@app.route("/listar_peliculas")
def listar_peliculas():
    peliculas = obtener_peliculas(lista_pelis)
    return render_template("listar.html", peliculas=peliculas)

@app.route("/resultado_personal")
def resultado_personal():
    nombre = session.get("nombre")
    hora_jugado = session.get("hora_jugado")
    puntaje = session.get("puntaje", "0/0")
    return render_template("resultado_personal.html", nombre=nombre, hora_jugado=hora_jugado, puntaje=puntaje)

@app.route("/resultados_globales")
def resultados_globales():
    return render_template("resultado_global.html", resultados=resultados)

@app.route("/ver_grafico")
def ver_grafico():
    resultados = session.get('resultados', [])
    nombre_archivo = 'grafico_torta.png'
    ruta_archivo = f'static/{nombre_archivo}'
    plt.savefig(ruta_archivo)
    
    return render_template("ver_graficos.html", ruta_archivo=nombre_archivo)


@app.route("/mostrar_grafica")
def mostrar_grafica():

    horas_juego = [datetime.strptime(resultado['hora'], "%H:%M:%S") for resultado in resultados]

    # Obtener los aciertos y desaciertos
    aciertos = [int(resultado['puntaje'].split('/')[0]) for resultado in resultados]
    desaciertos = [int(resultado['puntaje'].split('/')[1]) - int(resultado['puntaje'].split('/')[0]) for resultado in resultados]

    # Crear la gráfica
    plt.figure(figsize=(10, 6))

    # Curva de aciertos
    plt.plot(horas_juego, aciertos, label='Aciertos', marker='o')

    # Curva de desaciertos
    plt.plot(horas_juego, desaciertos, label='Desaciertos', marker='x')

    # Personalizar la gráfica
    plt.title('Aciertos y desaciertos en función de la hora de juego')
    plt.xlabel('Hora de juego')
    plt.ylabel('Cantidad')
    plt.legend()
    plt.grid(True)

    # Mostrar la gráfica
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(10, 6))
    plt.plot(horas_juego, aciertos, label='Aciertos', marker='o')
    plt.plot(horas_juego, desaciertos, label='Desaciertos', marker='x')
    plt.title('Aciertos y desaciertos en función de la hora de juego')
    plt.xlabel('Hora de juego')
    plt.ylabel('Cantidad')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convertir la gráfica a una imagen base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    img_url = f'data:image/png;base64,{img_base64}'

    # Pasar la URL de la imagen al HTML
    return render_template("mostrar_grafica.html", img_url=img_url)

@app.route("/mostrar_grafica_torta")
def mostrar_grafica_torta():
    horas_juego = [datetime.strptime(resultado['hora'], "%H:%M:%S") for resultado in resultados]

    # Obtener los aciertos y desaciertos
    aciertos = [int(resultado['puntaje'].split('/')[0]) for resultado in resultados]
    desaciertos = [int(resultado['puntaje'].split('/')[1]) - int(resultado['puntaje'].split('/')[0]) for resultado in resultados]

    # Crear el gráfico de torta
    plt.figure(figsize=(6, 6))
    total_aciertos = sum(aciertos)
    total_desaciertos = sum(desaciertos)
    plt.pie([total_aciertos, total_desaciertos], labels=['Aciertos', 'Desaciertos'], autopct='%1.1f%%', colors=['green', 'red'])
    plt.title('Gráfico de Torta de Aciertos y Desaciertos')
    plt.axis('equal')

    # Convertir la gráfica a una imagen base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    img_url = f'data:image/png;base64,{img_base64}'

    # Pasar la URL de la imagen al HTML
    return render_template("mostrar_grafica_torta.html", img_url=img_url)




if __name__ == "__main__":
    app.run(debug=True)