import tkinter as tk
import threading
from tkinter import scrolledtext, messagebox, Menu
from pystray import Icon, MenuItem as item
from PIL import Image, ImageDraw
from flask import Flask, render_template, request, jsonify, send_from_directory
import socket
import requests, os, json

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ipLocal = s.getsockname()[0]
    except Exception:
        ipLocal = '127.0.0.1'  # Si no puede obtener la IP, usa localhost
    finally:
        s.close()
    return ipLocal

# Mostrar la IP y el puerto en la interfaz gráfica
def update_status():
    ipLocal = get_local_ip()
    port = portServer  # Cambia esto según la variable porServer si la usas
    url = f"http://{ipLocal}:{port}"
    status_text.set(f"Servidor corriendo en: {url}\nNo cierre esta ventana.")

playing = None

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

app = Flask(__name__)

print(Colors.GREEN + "PARA LA GLORIA DE DIOS † ☝️" + Colors.END)
print()
print()
print(Colors.BLUE + "Iniciando el servidor..." + Colors.END)

# Ruta API para enviar la configuración como JSON
@app.route('/api/config')
def get_config():
    with open('config.json') as config_file:
        config_data = json.load(config_file)
    return jsonify(config_data)

# Cargar la configuración desde el archivo config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Obtener la IP y el token del archivo JSON
ip = config.get('ip')
token = config.get('token')
puerto = config.get('puerto')
portServer = config.get('portServer')

# Función para actualizar la configuración
def update_config():
    global ip, token, puerto, portServer
    ip = entry_ip.get()
    token = entry_token.get()
    puerto = entry_puerto.get()
    portServer = entry_portServer.get()

    # Guardar los valores en config.json
    with open('config.json', 'w') as config_file:
        json.dump({"ip": ip, "token": token, "puerto": puerto, "portServer": portServer}, config_file, indent=4)

    messagebox.showinfo("Información", "Configuración actualizada correctamente. Reinicie el servidor para aplicar los cambios.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/biblia')
def nueva_pagina():
    return render_template('Biblia.html')

# Ruta para servir bible.json
@app.route('/static/bible.json')
def bible_json():
    return send_from_directory('static', 'bible.json')

# Configuración para servir archivos estáticos (CSS, imágenes, etc.)
@app.route('/<path:path>')
def serve_static(path):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), path)

@app.route('/ToggleF8', methods=['POST'])
def ToggleF8():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ToggleF8?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"FONDO DE PANTALLA\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/ToggleF9', methods=['POST'])
def ToggleF9():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ToggleF9?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"SIN LETRA\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/ToggleF10', methods=['POST'])
def ToggleF10():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ToggleF10?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"PANTALLA NEGRA\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/actionNext', methods=['POST'])
def actionNext():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ActionNext?token={token}' # f'http://{ip}:{puerto}/api/ActionNext?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"SIGUIENTE\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/actionPrevious', methods=['POST'])
def actionPrevious():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/ActionPrevious?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"ANTERIOR\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/CloseCurrentPresentation', methods=['POST'])
def CloseCurrentPresentation():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/CloseCurrentPresentation?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"CERRAR PRESENTACION\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/GetMediaPlaylist', methods=['POST'])
def GetMediaPlaylist():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/GetMediaPlaylist?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"OBTENER PLAYLIST\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/MediaPlaylistAction', methods=['POST'])
def MediaPlaylistAction():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/MediaPlaylistAction?token={token}'
    headers = {'Content-Type': 'application/json'}

    # Obtener el dato del ID del elemento desde la solicitud POST
    data = request.get_json()
    element_id = data.get('id', '')

    # Crear los datos que se enviarán en el cuerpo de la solicitud POST
    data = {
        'id': element_id
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"PLAY\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

def GetMediaPlayerInfo():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/GetMediaPlayerInfo?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            data = response.json()

            global playing
            playing = data.get('data', {}).get('playing', None)
            log_message(f"El estado de reproducción es {playing}")
        else:
            return {'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text}
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/MediaPlayerActionPause', methods=['POST'])
def MediaPlayerActionPause():
    GetMediaPlayerInfo()
    client_ip = request.remote_addr

    if playing == True :
        url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
        headers = {'Content-Type': 'application/json'}
        data = {"action": "pause"}

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                log_message(f"Acción \"PAUSE\" ejecutada correctamente por {client_ip}")
                return jsonify(response.json())
            else:
                log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
                return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
        except Exception as e:
            log_message(f"Error desde {client_ip}: {str(e)}")
    
    else:
        url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
        headers = {'Content-Type': 'application/json'}
        data = {"action": "play"}

        try:
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                log_message(f"Acción \"PLAY\" ejecutada correctamente por {client_ip}")
                return jsonify(response.json())
            else:
                log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
                return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
        except Exception as e:
            log_message(f"Error desde {client_ip}: {str(e)}")

@app.route('/MediaPlayerActionStop', methods=['POST'])
def MediaPlayerActionStop():
    client_ip = request.remote_addr
    url = f'http://{ip}:{puerto}/api/MediaPlayerAction?token={token}'
    headers = {'Content-Type': 'application/json'}
    data = {"action": "stop"}

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            log_message(f"Acción \"STOP\" ejecutada correctamente por {client_ip}")
            return jsonify(response.json())
        else:
            log_message(f"Error al realizar la solicitud desde {client_ip}: {response.status_code}")
            return jsonify({'error': 'Error al realizar la solicitud', 'status_code': response.status_code, 'text': response.text})
    except Exception as e:
        log_message(f"Error desde {client_ip}: {str(e)}")

# Configurar la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Server - Holyrics Web Control")
root.resizable(False, False)

def show_about():
    about_message = (
        "☝️ PARA LA GLORIA DE DIOS ☝️\n\n"
        "Web Control para Holyrics\n"
        "Versión: 2.0.0\n\n\n"
        "Información de contacto:\n\n"
        "Telegram: @mark_ost7\n"
        "GitHub: https://github.com/wcmark\n"
        "YouTube personal: @Marcos-Tapia\n"
        "YouTube de la iglesia: @ice-lapaz\n\n"
        "San Miguel del Monte, Bs. As. - Argentina\n"
    )
    messagebox.showinfo("Acerca de...", about_message)

# Función para crear el ícono de la bandeja (simple ejemplo con un círculo)
def create_image():
    # Crear una imagen de 64x64
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill='black')
    return image

# Función que muestra nuevamente la ventana de Tkinter
def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

# Función que oculta la ventana de Tkinter y muestra el ícono en la bandeja
def hide_window():
    root.withdraw()  # Ocultar la ventana principal
    image = create_image()  # Crear un ícono
    menu = (item('Mostrar', show_window), item('Salir', close_cmd))
    icon = Icon("AppName", image, "My App", menu)
    threading.Thread(target=icon.run, daemon=True).start()

"""
# Función para salir completamente de la aplicación
def quit_app(icon, item):
    icon.stop()
    root.quit()
"""

def close_cmd():
    # Cierra la ventana de CMD y finaliza la ejecución de Flask
    os._exit(0)

root.protocol("WM_DELETE_WINDOW", close_cmd)

# Crear el menú
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Añadir la opción de minimizar al área de notificaciones
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Minimizar a la bandeja del sistema", command=hide_window)
menu_bar.add_cascade(label="Opciones", menu=file_menu)

# Agregar el menú "Ayuda"
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ayuda", menu=help_menu)
help_menu.add_command(label="Acerca de...", command=show_about)

# Campos para config.json
tk.Label(root, text="IP del equipo de Holyrics:").grid(row=0, column=0, padx=10, pady=10, sticky="W")
entry_ip = tk.Entry(root)
entry_ip.grid(row=0, column=1, padx=5, pady=10)
entry_ip.insert(0, ip)

tk.Label(root, text="Token de API Holyrics.\n (Habilitar y configurar permisos):").grid(row=1, column=0, padx=10, pady=10, sticky="W")
entry_token = tk.Entry(root, show="*")
entry_token.grid(row=1, column=1, padx=5, pady=10)
entry_token.insert(0, token)

tk.Label(root, text="Puerto (API Holyrics), por defecto 8091:").grid(row=2, column=0, padx=10, pady=10, sticky="W")
entry_puerto = tk.Entry(root)
entry_puerto.grid(row=2, column=1, padx=5, pady=10)
entry_puerto.insert(0, puerto)

tk.Label(root, text="Puerto para este servidor, por defecto 5000:").grid(row=3, column=0, padx=10, pady=10, sticky="W")
entry_portServer = tk.Entry(root)
entry_portServer.grid(row=3, column=1, padx=5, pady=10)
entry_portServer.insert(0, portServer)

# Botón para guardar configuración
btn_save = tk.Button(root, text="Guardar Configuración", command=update_config)
btn_save.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Campo de texto grande para mensajes/errores
tk.Label(root, text="Logs:").grid(row=6, column=0, padx=10, pady=0, sticky="w")
txt_logs = scrolledtext.ScrolledText(root, width=40, height=10)
txt_logs.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

def log_message(message):
    txt_logs.insert(tk.END, message + '\n')
    txt_logs.see(tk.END)

# Ejemplo de cómo agregar un mensaje de log
log_message("Servidor en ejecución...")

# Etiqueta para mostrar el estado del servidor
status_text = tk.StringVar()
status_label = tk.Label(root, textvariable=status_text, font=("Helvetica", 12))
status_label.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Actualizar el estado en la interfaz gráfica
update_status()


if __name__ == '__main__':
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=portServer, debug=False))
    flask_thread.start()

    root.mainloop()