from flask import Flask, render_template_string
from datetime import datetime
from LogicaAgenda import crear_agenda, obtener_participantes, generar_registro_discusion, agenda

app = Flask(__name__)

# Ruta principal
@app.route('/')
def generar_agenda():
    # Crear la instancia de la agenda
    crear_agenda()
    
    # Obtener la descripción y fecha de la agenda
    descripcion = agenda.descripcion
    fecha = datetime.now().strftime("%d-%m-%Y")

    # Obtener la lista de participantes
    participantes = obtener_participantes()

    # Generar el registro de discusión
    registro_discusion = generar_registro_discusion()

    # Renderizar la plantilla HTML con los datos
    return render_template_string('Agenda.html', descripcion=descripcion, fecha=fecha, participantes=participantes, registro_discusion=registro_discusion)

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)