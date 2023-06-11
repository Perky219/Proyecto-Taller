import webview

pass


def generar_html(lista_elementos):
    # Crea la estructura básica del HTML
    html = """<html><head>
                <meta charset="UTF-8 \">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Agenda 23-05-23</title>
                </head><body>"""
    
    html=html+'<ol>'
    # Genera el contenido basado en la lista de elementos
    for elemento in lista_elementos:
        html += f"<li>{elemento}</li>"
    
    # Cierra las etiquetas del HTML
    html=html+'</ol>'
    html += "</body></html>"
    
    # Devuelve el código HTML generado
    return html

def mostrar_html_en_ventana(codigo_html):
    # Crea una ventana y carga el contenido HTML
    webview.create_window("Visor HTML", html=codigo_html)

    # Inicia el bucle de la aplicación
    webview.start()

# Ejemplo de lista de elementos
lista = ["Elemento 1 ", "Elemento 2", "Elemento 3"]

# Genera el código HTML utilizando la función anterior
codigo_html_generado = generar_html(lista)

# Genera el código HTML utilizando la función anterior
file= open("sesion.html", 'tr')

sesion01_html = file.read()

# Muestra el código HTML en una ventana
mostrar_html_en_ventana(codigo_html_generado)
mostrar_html_en_ventana(sesion01_html)