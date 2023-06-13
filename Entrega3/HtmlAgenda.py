from flask import Flask, render_template_string # Importar Flask y render_template_string
from datetime import datetime # Importar datetime
from LogicaAgenda import crear_agenda, obtener_participantes, generar_registro_discusion, agenda # Importar las funciones de la lógica de la agenda

app = Flask(__name__) # Crear la instancia de la aplicación Flask

# Ruta principal
@app.route('/') # Decorador de ruta
def generar_agenda():
    """
    Función que genera la agenda en formato HTML

    Returns:
        str: Plantilla HTML con la agenda
    """
    # Crear instancia de la agenda
    crear_agenda() # Llamada a la función de la lógica de la agenda
    
    # Obtener la descripción y fecha de la agenda
    descripcion = agenda.descripcion # Descripción de la agenda
    fecha = datetime.now().strftime("%d-%m-%Y") # Fecha de la agenda

    # Obtener la lista de participantes
    participantes = obtener_participantes() # Llamada a la función de la lógica de la agenda

    # Generar el registro de discusión
    registro_discusion = generar_registro_discusion() # Llamada a la función de la lógica de la agenda

    # Renderizar la plantilla HTML con los datos
    return render_template_string('Agenda.html', descripcion=descripcion, fecha=fecha, participantes=participantes, registro_discusion=registro_discusion) # Llamada a la función de la lógica de la agenda

# Ejecutar la aplicación Flask
if __name__ == '__main__': # Si el script se ejecuta directamente
    app.run(debug=True) # Ejecutar la aplicación Flask en modo debug